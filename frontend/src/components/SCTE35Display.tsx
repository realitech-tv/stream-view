import { useState } from 'react';
import type { SCTE35Marker } from '../types/api';

interface SCTE35DisplayProps {
  markers: SCTE35Marker[];
}

const SCTE35Display = ({ markers }: SCTE35DisplayProps) => {
  const [expandedRows, setExpandedRows] = useState<Set<number>>(new Set());

  if (!markers || markers.length === 0) {
    return (
      <div className="text-sm text-gray-500 italic">
        No SCTE-35 markers found
      </div>
    );
  }

  const toggleRow = (index: number) => {
    const newExpanded = new Set(expandedRows);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedRows(newExpanded);
  };

  const formatPTS = (pts?: number): string => {
    if (pts === undefined || pts === null) return '-';
    return `${(pts / 90000).toFixed(3)}s`;
  };

  const formatDuration = (duration?: number): string => {
    if (duration === undefined || duration === null) return '-';
    return `${(duration / 90000).toFixed(3)}s`;
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-10">

            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Event ID
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              PTS
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Command
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Duration
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              UPID
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {markers.map((marker, index) => (
            <>
              <tr
                key={index}
                className={`${index % 2 === 0 ? 'bg-white' : 'bg-gray-50'} cursor-pointer hover:bg-gray-100`}
                onClick={() => toggleRow(index)}
              >
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                  <svg
                    className={`w-4 h-4 transition-transform ${expandedRows.has(index) ? 'transform rotate-90' : ''}`}
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
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                  {marker.event_id ?? '-'}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                  {formatPTS(marker.pts)}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                  {marker.command || '-'}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                  {formatDuration(marker.duration)}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                  {marker.upid || '-'}
                </td>
              </tr>
              {expandedRows.has(index) && (
                <tr key={`${index}-details`} className={index % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
                  <td colSpan={6} className="px-4 py-4">
                    <div className="ml-8 space-y-2 text-sm">
                      <h5 className="font-semibold text-gray-700 mb-2">Detailed Information</h5>
                      <div className="grid grid-cols-2 gap-4">
                        {marker.segmentation_type && (
                          <div>
                            <span className="font-medium text-gray-600">Segmentation Type: </span>
                            <span className="text-gray-900">{marker.segmentation_type}</span>
                          </div>
                        )}
                        {marker.segment_num !== undefined && (
                          <div>
                            <span className="font-medium text-gray-600">Segment Number: </span>
                            <span className="text-gray-900">{marker.segment_num}</span>
                          </div>
                        )}
                        {marker.segments_expected !== undefined && (
                          <div>
                            <span className="font-medium text-gray-600">Segments Expected: </span>
                            <span className="text-gray-900">{marker.segments_expected}</span>
                          </div>
                        )}
                        {marker.pre_roll !== undefined && (
                          <div>
                            <span className="font-medium text-gray-600">Pre-roll: </span>
                            <span className="text-gray-900">{formatDuration(marker.pre_roll)}</span>
                          </div>
                        )}
                        {marker.out_of_network !== undefined && (
                          <div>
                            <span className="font-medium text-gray-600">Out of Network: </span>
                            <span className="text-gray-900">{marker.out_of_network ? 'Yes' : 'No'}</span>
                          </div>
                        )}
                        {marker.auto_return !== undefined && (
                          <div>
                            <span className="font-medium text-gray-600">Auto Return: </span>
                            <span className="text-gray-900">{marker.auto_return ? 'Yes' : 'No'}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  </td>
                </tr>
              )}
            </>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default SCTE35Display;
