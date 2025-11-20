"""
SCTE-35 parser service.

Extracts and parses SCTE-35 markers from HLS and DASH manifests.
"""

import base64
from typing import List, Dict, Any
from xml.etree import ElementTree as ET

try:
    import threefive
    THREEFIVE_AVAILABLE = True
except ImportError:
    THREEFIVE_AVAILABLE = False

from models.schemas import SCTE35Marker


def parse_scte35_data(scte35_data: str, encoding: str = 'base64') -> Dict[str, Any]:
    """
    Parse SCTE-35 binary data using threefive library.

    Args:
        scte35_data: SCTE-35 data (base64 or hex encoded)
        encoding: Encoding type ('base64' or 'hex')

    Returns:
        Dictionary containing parsed SCTE-35 information
    """
    if not THREEFIVE_AVAILABLE:
        return {
            'error': 'threefive library not available',
            'raw_data': scte35_data
        }

    try:
        # Decode the SCTE-35 data
        if encoding == 'base64':
            # threefive can handle base64 directly
            cue = threefive.Cue(scte35_data)
        else:
            # For hex, convert to bytes
            scte35_bytes = bytes.fromhex(scte35_data)
            cue = threefive.Cue(scte35_bytes)

        # Decode the cue
        cue.decode()

        # Extract command information
        command_info = {}
        if hasattr(cue, 'command'):
            cmd = cue.command
            command_info = {
                'command_type': cmd.command_type if hasattr(cmd, 'command_type') else None,
                'pts': cmd.pts_time if hasattr(cmd, 'pts_time') else None,
                'command_length': cmd.command_length if hasattr(cmd, 'command_length') else None
            }

            # Splice Insert specific fields
            if hasattr(cmd, 'splice_event_id'):
                command_info['event_id'] = cmd.splice_event_id
            if hasattr(cmd, 'out_of_network_indicator'):
                command_info['out_of_network'] = cmd.out_of_network_indicator
            if hasattr(cmd, 'program_splice_flag'):
                command_info['program_splice_flag'] = cmd.program_splice_flag
            if hasattr(cmd, 'duration_flag'):
                command_info['duration_flag'] = cmd.duration_flag
            if hasattr(cmd, 'break_duration'):
                command_info['break_duration'] = cmd.break_duration
            if hasattr(cmd, 'auto_return'):
                command_info['auto_return'] = cmd.auto_return
            if hasattr(cmd, 'splice_immediate_flag'):
                command_info['splice_immediate_flag'] = cmd.splice_immediate_flag

        # Extract descriptor information
        descriptors = []
        if hasattr(cue, 'descriptors'):
            for desc in cue.descriptors:
                desc_info = {
                    'tag': desc.tag if hasattr(desc, 'tag') else None,
                }

                # Segmentation descriptor
                if hasattr(desc, 'segmentation_event_id'):
                    desc_info['segmentation_event_id'] = desc.segmentation_event_id
                if hasattr(desc, 'segmentation_type_id'):
                    desc_info['segmentation_type_id'] = desc.segmentation_type_id
                if hasattr(desc, 'segment_num'):
                    desc_info['segment_num'] = desc.segment_num
                if hasattr(desc, 'segments_expected'):
                    desc_info['segments_expected'] = desc.segments_expected
                if hasattr(desc, 'segmentation_duration'):
                    desc_info['segmentation_duration'] = desc.segmentation_duration
                if hasattr(desc, 'segmentation_upid'):
                    desc_info['segmentation_upid'] = desc.segmentation_upid
                if hasattr(desc, 'segmentation_upid_type'):
                    desc_info['segmentation_upid_type'] = desc.segmentation_upid_type

                descriptors.append(desc_info)

        return {
            'command': command_info,
            'descriptors': descriptors,
            'info_section': {
                'table_id': cue.info_section.table_id if hasattr(cue, 'info_section') else None,
                'protocol_version': cue.info_section.protocol_version if hasattr(cue, 'info_section') else None
            }
        }

    except Exception as e:
        return {
            'error': str(e),
            'raw_data': scte35_data
        }


def extract_hls_scte35(playlist: Any) -> List[SCTE35Marker]:
    """
    Extract SCTE-35 markers from HLS manifest.

    Args:
        playlist: Parsed M3U8 playlist object

    Returns:
        List of SCTE35Marker objects
    """
    markers = []

    # Check for SCTE-35 in segments (EXT-X-SCTE35 tags)
    if hasattr(playlist, 'segments') and playlist.segments:
        for segment in playlist.segments:
            # Check for SCTE-35 cue out/in
            if hasattr(segment, 'scte35'):
                scte35_data = segment.scte35
                parsed = parse_scte35_data(scte35_data)

                if 'error' not in parsed:
                    cmd = parsed.get('command', {})
                    descs = parsed.get('descriptors', [])

                    # Extract main descriptor info
                    seg_type = None
                    upid = None
                    duration = None
                    event_id = None

                    if descs:
                        desc = descs[0]
                        seg_type_id = desc.get('segmentation_type_id')
                        if seg_type_id:
                            # Map segmentation type ID to description
                            seg_type = f"Type {seg_type_id}"
                        upid = desc.get('segmentation_upid')
                        seg_duration = desc.get('segmentation_duration')
                        if seg_duration:
                            duration = seg_duration / 90000.0  # Convert to seconds
                        event_id = desc.get('segmentation_event_id')

                    if not event_id:
                        event_id = cmd.get('event_id')

                    marker = SCTE35Marker(
                        event_id=event_id,
                        pts=cmd.get('pts'),
                        command_type=cmd.get('command_type', 'unknown'),
                        duration=duration,
                        upid=upid,
                        segmentation_type=seg_type,
                        out_of_network=cmd.get('out_of_network', False),
                        auto_return=cmd.get('auto_return', False),
                        pre_roll=None
                    )
                    markers.append(marker)

            # Check for SCTE-35 in DATERANGE tags
            if hasattr(segment, 'dateranges') and segment.dateranges:
                for daterange in segment.dateranges:
                    if hasattr(daterange, 'scte35_cmd') or hasattr(daterange, 'scte35_out') or hasattr(daterange, 'scte35_in'):
                        # Extract SCTE-35 data from daterange
                        scte35_cmd = getattr(daterange, 'scte35_cmd', None)
                        scte35_out = getattr(daterange, 'scte35_out', None)
                        scte35_in = getattr(daterange, 'scte35_in', None)

                        scte35_data = scte35_cmd or scte35_out or scte35_in
                        if scte35_data:
                            parsed = parse_scte35_data(scte35_data)

                            if 'error' not in parsed:
                                cmd = parsed.get('command', {})
                                descs = parsed.get('descriptors', [])

                                marker = SCTE35Marker(
                                    event_id=cmd.get('event_id'),
                                    pts=cmd.get('pts'),
                                    command_type=cmd.get('command_type', 'unknown'),
                                    duration=getattr(daterange, 'duration', None),
                                    upid=descs[0].get('segmentation_upid') if descs else None,
                                    segmentation_type=descs[0].get('segmentation_type_id') if descs else None,
                                    out_of_network=cmd.get('out_of_network', False),
                                    auto_return=cmd.get('auto_return', False),
                                    pre_roll=None
                                )
                                markers.append(marker)

    return markers


def extract_dash_scte35(root: ET.Element, namespaces: Dict[str, str]) -> List[SCTE35Marker]:
    """
    Extract SCTE-35 markers from DASH manifest.

    Args:
        root: MPD root element
        namespaces: XML namespaces

    Returns:
        List of SCTE35Marker objects
    """
    markers = []

    # Look for EventStream elements with SCTE-35 scheme
    scte35_schemes = [
        'urn:scte:scte35:2013:bin',
        'urn:scte:scte35:2014:xml+bin',
        'urn:scte:scte35:2013:xml'
    ]

    for period in root.findall('.//mpd:Period', namespaces):
        for event_stream in period.findall('.//mpd:EventStream', namespaces):
            scheme_id_uri = event_stream.get('schemeIdUri', '')

            # Check if this is a SCTE-35 event stream
            if any(scheme in scheme_id_uri for scheme in scte35_schemes):
                # Extract events
                for event in event_stream.findall('.//mpd:Event', namespaces):
                    presentation_time = event.get('presentationTime')
                    duration = event.get('duration')
                    event_id = event.get('id')

                    # Event data might be in text content or Signal element
                    scte35_data = None
                    if event.text:
                        scte35_data = event.text.strip()
                    else:
                        # Look for Signal/Binary element
                        signal = event.find('.//scte35:Signal', namespaces)
                        if signal is not None:
                            binary = signal.find('.//scte35:Binary', namespaces)
                            if binary is not None and binary.text:
                                scte35_data = binary.text.strip()

                    if scte35_data:
                        parsed = parse_scte35_data(scte35_data)

                        if 'error' not in parsed:
                            cmd = parsed.get('command', {})
                            descs = parsed.get('descriptors', [])

                            # Convert duration from timescale to seconds
                            duration_sec = None
                            if duration:
                                timescale = event_stream.get('timescale', '1')
                                try:
                                    duration_sec = float(duration) / float(timescale)
                                except:
                                    pass

                            # Convert presentation time
                            pts = None
                            if presentation_time:
                                try:
                                    pts = int(presentation_time)
                                except:
                                    pass

                            marker = SCTE35Marker(
                                event_id=event_id or cmd.get('event_id'),
                                pts=pts or cmd.get('pts'),
                                command_type=cmd.get('command_type', 'unknown'),
                                duration=duration_sec,
                                upid=descs[0].get('segmentation_upid') if descs else None,
                                segmentation_type=descs[0].get('segmentation_type_id') if descs else None,
                                out_of_network=cmd.get('out_of_network', False),
                                auto_return=cmd.get('auto_return', False),
                                pre_roll=None
                            )
                            markers.append(marker)

    return markers


async def extract_scte35_markers(url: str, manifest_type: str, parsed_data: Dict) -> List[SCTE35Marker]:
    """
    Extract SCTE-35 markers from manifest.

    Args:
        url: Manifest URL
        manifest_type: Type of manifest ('hls' or 'dash')
        parsed_data: Parsed manifest data

    Returns:
        List of SCTE35Marker objects
    """
    try:
        if manifest_type == 'hls':
            playlist = parsed_data.get('raw_playlist')
            if playlist:
                return extract_hls_scte35(playlist)
        elif manifest_type == 'dash':
            root = parsed_data.get('raw_xml')
            namespaces = parsed_data.get('namespaces', {})
            if root is not None:
                return extract_dash_scte35(root, namespaces)

        return []

    except Exception as e:
        # Log error but don't fail the entire request
        print(f"Error extracting SCTE-35 markers: {e}")
        return []
