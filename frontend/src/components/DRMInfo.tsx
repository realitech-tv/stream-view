import type { DRMInfo as DRMInfoType } from '../types/api';

interface DRMInfoProps {
  drmInfo?: DRMInfoType;
}

const DRMInfo = ({ drmInfo }: DRMInfoProps) => {
  if (!drmInfo || (!drmInfo.scheme && !drmInfo.method && !drmInfo.key_system)) {
    return (
      <div className="flex items-center px-4 py-3 bg-green-50 border border-green-200 rounded-lg">
        <svg
          className="w-5 h-5 text-green-500 mr-3"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fillRule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
            clipRule="evenodd"
          />
        </svg>
        <span className="text-sm font-medium text-green-800">No DRM detected</span>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center px-4 py-3 bg-yellow-50 border border-yellow-200 rounded-lg">
        <svg
          className="w-5 h-5 text-yellow-500 mr-3"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fillRule="evenodd"
            d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z"
            clipRule="evenodd"
          />
        </svg>
        <span className="text-sm font-medium text-yellow-800">DRM Protected Content</span>
      </div>

      <div className="bg-gray-50 rounded-lg p-4 space-y-2">
        {drmInfo.scheme && (
          <div className="flex">
            <span className="text-sm font-medium text-gray-700 w-32">Scheme:</span>
            <span className="text-sm text-gray-900">{drmInfo.scheme}</span>
          </div>
        )}
        {drmInfo.method && (
          <div className="flex">
            <span className="text-sm font-medium text-gray-700 w-32">Method:</span>
            <span className="text-sm text-gray-900">{drmInfo.method}</span>
          </div>
        )}
        {drmInfo.key_system && (
          <div className="flex">
            <span className="text-sm font-medium text-gray-700 w-32">Key System:</span>
            <span className="text-sm text-gray-900">{drmInfo.key_system}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default DRMInfo;
