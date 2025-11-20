import type { BitrateInfo } from '../types/api';

interface BitrateTableProps {
  bitrates: BitrateInfo[];
}

const BitrateTable = ({ bitrates }: BitrateTableProps) => {
  if (!bitrates || bitrates.length === 0) {
    return (
      <div className="text-sm text-gray-500 italic">
        No bitrate information available
      </div>
    );
  }

  const formatBitrate = (bitrate: number): string => {
    if (bitrate >= 1_000_000) {
      return `${(bitrate / 1_000_000).toFixed(2)} Mbps`;
    }
    return `${(bitrate / 1_000).toFixed(0)} Kbps`;
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Level
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Property
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Value
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {bitrates.map((bitrate, index) => {
            const properties = [];

            if (bitrate.resolution) {
              properties.push({ property: 'Resolution', value: bitrate.resolution });
            }
            if (bitrate.codec) {
              properties.push({ property: 'Codec', value: bitrate.codec });
            }
            properties.push({ property: 'Bitrate', value: formatBitrate(bitrate.bitrate) });
            if (bitrate.frame_rate) {
              properties.push({ property: 'Frame Rate', value: `${bitrate.frame_rate} fps` });
            }
            if (bitrate.level) {
              properties.push({ property: 'Level', value: bitrate.level });
            }

            return properties.map((prop, propIndex) => (
              <tr
                key={`${index}-${propIndex}`}
                className={propIndex % 2 === 0 ? 'bg-white' : 'bg-gray-50'}
              >
                <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                  {propIndex === 0 ? `Level ${index + 1}` : ''}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                  {prop.property}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">
                  {prop.value}
                </td>
              </tr>
            ));
          })}
        </tbody>
      </table>
    </div>
  );
};

export default BitrateTable;
