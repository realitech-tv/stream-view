import type { VideoMetadata as VideoMetadataType } from '../types/api';

interface VideoMetadataProps {
  metadata: VideoMetadataType[];
}

const VideoMetadata = ({ metadata }: VideoMetadataProps) => {
  if (!metadata || metadata.length === 0) {
    return (
      <div className="text-sm text-gray-500 italic">
        No video metadata available
      </div>
    );
  }

  const formatBitrate = (bitrate?: number): string => {
    if (!bitrate) return '-';
    if (bitrate >= 1_000_000) {
      return `${(bitrate / 1_000_000).toFixed(2)} Mbps`;
    }
    return `${(bitrate / 1_000).toFixed(0)} Kbps`;
  };

  const formatFileSize = (size?: number): string => {
    if (!size) return '-';
    if (size >= 1_000_000) {
      return `${(size / 1_000_000).toFixed(2)} MB`;
    }
    return `${(size / 1_000).toFixed(0)} KB`;
  };

  const formatDuration = (duration?: number): string => {
    if (!duration) return '-';
    return `${duration.toFixed(2)}s`;
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Bitrate Level
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Container
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Codec
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Profile
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Resolution
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              FPS
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Color Space
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Bit Rate
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Fragment Duration
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              File Size
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {metadata.map((item, index) => (
            <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
              <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                {item.bitrate_level || '-'}
              </td>
              <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                {item.container || '-'}
              </td>
              <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                {item.codec || '-'}
              </td>
              <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                {item.profile || '-'}
              </td>
              <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                {item.resolution || '-'}
              </td>
              <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                {item.fps ? `${item.fps} fps` : '-'}
              </td>
              <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                {item.color_space || '-'}
              </td>
              <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                {formatBitrate(item.bit_rate)}
              </td>
              <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                {formatDuration(item.fragment_duration)}
              </td>
              <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                {formatFileSize(item.file_size)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default VideoMetadata;
