import type { AudioTrack, SubtitleTrack, ThumbnailTrack } from '../types/api';

interface TrackInfoProps {
  audioTracks: AudioTrack[];
  subtitleTracks: SubtitleTrack[];
  thumbnailTracks: ThumbnailTrack[];
}

const TrackInfo = ({ audioTracks, subtitleTracks, thumbnailTracks }: TrackInfoProps) => {
  const hasAudio = audioTracks && audioTracks.length > 0;
  const hasSubtitles = subtitleTracks && subtitleTracks.length > 0;
  const hasThumbnails = thumbnailTracks && thumbnailTracks.length > 0;

  if (!hasAudio && !hasSubtitles && !hasThumbnails) {
    return (
      <div className="text-sm text-gray-500 italic">
        No track information available
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Audio Tracks */}
      {hasAudio && (
        <div>
          <h4 className="text-sm font-semibold text-gray-700 mb-3">Audio Tracks</h4>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                    Language
                  </th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                    Name
                  </th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                    Codec
                  </th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                    Channels
                  </th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                    Bitrate
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {audioTracks.map((track, index) => (
                  <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                    <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-900">
                      {track.language || '-'}
                    </td>
                    <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-700">
                      {track.name || '-'}
                    </td>
                    <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-700">
                      {track.codec || '-'}
                    </td>
                    <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-700">
                      {track.channels || '-'}
                    </td>
                    <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-700">
                      {track.bitrate ? `${(track.bitrate / 1000).toFixed(0)} Kbps` : '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Subtitle Tracks */}
      {hasSubtitles && (
        <div>
          <h4 className="text-sm font-semibold text-gray-700 mb-3">Subtitle Tracks</h4>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                    Language
                  </th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                    Name
                  </th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                    Format
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {subtitleTracks.map((track, index) => (
                  <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                    <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-900">
                      {track.language || '-'}
                    </td>
                    <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-700">
                      {track.name || '-'}
                    </td>
                    <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-700">
                      {track.format || '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Thumbnail Tracks */}
      {hasThumbnails && (
        <div>
          <h4 className="text-sm font-semibold text-gray-700 mb-3">Thumbnail Tracks</h4>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                    Resolution
                  </th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                    Interval
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {thumbnailTracks.map((track, index) => (
                  <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                    <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-900">
                      {track.resolution || '-'}
                    </td>
                    <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-700">
                      {track.interval ? `${track.interval}s` : '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default TrackInfo;
