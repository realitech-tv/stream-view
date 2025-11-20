export interface BitrateInfo {
  resolution?: string;
  codec?: string;
  bitrate: number;
  frame_rate?: number;
  level?: string;
}

export interface AudioTrack {
  language?: string;
  name?: string;
  codec?: string;
  channels?: number;
  bitrate?: number;
}

export interface SubtitleTrack {
  language?: string;
  name?: string;
  format?: string;
}

export interface ThumbnailTrack {
  resolution?: string;
  interval?: number;
}

export interface DRMInfo {
  scheme?: string;
  method?: string;
  key_system?: string;
}

export interface SCTE35Marker {
  event_id?: number;
  pts?: number;
  command?: string;
  duration?: number;
  upid?: string;
  segmentation_type?: string;
  segment_num?: number;
  segments_expected?: number;
  pre_roll?: number;
  out_of_network?: boolean;
  auto_return?: boolean;
}

export interface VideoMetadata {
  bitrate_level?: string;
  container?: string;
  codec?: string;
  profile?: string;
  resolution?: string;
  fps?: number;
  color_space?: string;
  bit_rate?: number;
  fragment_duration?: number;
  file_size?: number;
}

export interface AnalyzeResponse {
  manifest_type: 'hls' | 'dash';
  bitrates: BitrateInfo[];
  audio_tracks: AudioTrack[];
  subtitle_tracks: SubtitleTrack[];
  thumbnail_tracks: ThumbnailTrack[];
  drm_info?: DRMInfo;
  scte35_markers: SCTE35Marker[];
  video_metadata: VideoMetadata[];
}

export interface AnalyzeRequest {
  url: string;
}

export interface ErrorResponse {
  detail: string;
}
