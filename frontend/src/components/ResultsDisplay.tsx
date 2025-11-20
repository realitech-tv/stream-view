import { useState } from 'react';
import type { AnalyzeResponse } from '../types/api';
import BitrateTable from './BitrateTable';
import TrackInfo from './TrackInfo';
import DRMInfo from './DRMInfo';
import SCTE35Display from './SCTE35Display';
import VideoMetadata from './VideoMetadata';

interface ResultsDisplayProps {
  data: AnalyzeResponse;
}

interface Section {
  id: string;
  title: string;
  isCollapsible: boolean;
}

const ResultsDisplay = ({ data }: ResultsDisplayProps) => {
  const [collapsedSections, setCollapsedSections] = useState<Set<string>>(new Set());

  const sections: Section[] = [
    { id: 'overview', title: 'Overview', isCollapsible: true },
    { id: 'bitrates', title: 'Bitrate Levels', isCollapsible: true },
    { id: 'tracks', title: 'Tracks', isCollapsible: true },
    { id: 'drm', title: 'DRM Information', isCollapsible: true },
    { id: 'scte35', title: 'SCTE-35 Markers', isCollapsible: true },
    { id: 'video', title: 'Video Analysis', isCollapsible: true },
  ];

  const toggleSection = (sectionId: string) => {
    const newCollapsed = new Set(collapsedSections);
    if (newCollapsed.has(sectionId)) {
      newCollapsed.delete(sectionId);
    } else {
      newCollapsed.add(sectionId);
    }
    setCollapsedSections(newCollapsed);
  };

  const SectionHeader = ({ section }: { section: Section }) => (
    <div
      className={`flex items-center justify-between px-6 py-4 bg-gray-100 border-b border-gray-200 ${
        section.isCollapsible ? 'cursor-pointer hover:bg-gray-150' : ''
      }`}
      onClick={() => section.isCollapsible && toggleSection(section.id)}
    >
      <h3 className="text-lg font-semibold text-gray-800">{section.title}</h3>
      {section.isCollapsible && (
        <svg
          className={`w-5 h-5 text-gray-600 transition-transform ${
            collapsedSections.has(section.id) ? '' : 'transform rotate-90'
          }`}
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fillRule="evenodd"
            d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
            clipRule="evenodd"
          />
        </svg>
      )}
    </div>
  );

  return (
    <div className="w-full max-w-6xl mx-auto px-6 py-8">
      <div className="bg-white rounded-lg shadow-lg border border-gray-200 overflow-hidden">
        {/* Overview Section */}
        <SectionHeader section={sections[0]} />
        {!collapsedSections.has('overview') && (
          <div className="px-6 py-4 space-y-3">
            <div className="flex items-center">
              <span className="text-sm font-medium text-gray-600 w-40">Manifest Type:</span>
              <span className="text-sm text-gray-900 uppercase font-semibold">
                {data.manifest_type}
              </span>
            </div>
            <div className="flex items-center">
              <span className="text-sm font-medium text-gray-600 w-40">Bitrate Levels:</span>
              <span className="text-sm text-gray-900">{data.bitrates.length}</span>
            </div>
            <div className="flex items-center">
              <span className="text-sm font-medium text-gray-600 w-40">Audio Tracks:</span>
              <span className="text-sm text-gray-900">{data.audio_tracks.length}</span>
            </div>
            <div className="flex items-center">
              <span className="text-sm font-medium text-gray-600 w-40">Subtitle Tracks:</span>
              <span className="text-sm text-gray-900">{data.subtitle_tracks.length}</span>
            </div>
            <div className="flex items-center">
              <span className="text-sm font-medium text-gray-600 w-40">SCTE-35 Markers:</span>
              <span className="text-sm text-gray-900">{data.scte35_markers.length}</span>
            </div>
          </div>
        )}

        {/* Bitrates Section */}
        <SectionHeader section={sections[1]} />
        {!collapsedSections.has('bitrates') && (
          <div className="px-6 py-4">
            <BitrateTable bitrates={data.bitrates} />
          </div>
        )}

        {/* Tracks Section */}
        <SectionHeader section={sections[2]} />
        {!collapsedSections.has('tracks') && (
          <div className="px-6 py-4">
            <TrackInfo
              audioTracks={data.audio_tracks}
              subtitleTracks={data.subtitle_tracks}
              thumbnailTracks={data.thumbnail_tracks}
            />
          </div>
        )}

        {/* DRM Section */}
        <SectionHeader section={sections[3]} />
        {!collapsedSections.has('drm') && (
          <div className="px-6 py-4">
            <DRMInfo drmInfo={data.drm_info} />
          </div>
        )}

        {/* SCTE-35 Section */}
        <SectionHeader section={sections[4]} />
        {!collapsedSections.has('scte35') && (
          <div className="px-6 py-4">
            <SCTE35Display markers={data.scte35_markers} />
          </div>
        )}

        {/* Video Analysis Section */}
        <SectionHeader section={sections[5]} />
        {!collapsedSections.has('video') && (
          <div className="px-6 py-4">
            <VideoMetadata metadata={data.video_metadata} />
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultsDisplay;
