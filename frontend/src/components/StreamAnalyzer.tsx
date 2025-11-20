import { useState } from 'react';
import type { AnalyzeResponse } from '../types/api';

interface StreamAnalyzerProps {
  onAnalyze: (data: AnalyzeResponse) => void;
  onError: (error: string) => void;
}

const StreamAnalyzer = ({ onAnalyze, onError }: StreamAnalyzerProps) => {
  const [url, setUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [validationError, setValidationError] = useState('');

  const validateUrl = (urlString: string): boolean => {
    setValidationError('');

    if (!urlString.trim()) {
      setValidationError('Please enter a URL');
      return false;
    }

    // Check if it's a valid URL
    try {
      const urlObj = new URL(urlString);
      if (!urlObj.protocol.startsWith('http')) {
        setValidationError('URL must use HTTP or HTTPS protocol');
        return false;
      }
    } catch {
      setValidationError('Please enter a valid URL');
      return false;
    }

    // Check if URL ends with .m3u8 or .mpd
    const lowerUrl = urlString.toLowerCase();
    if (!lowerUrl.endsWith('.m3u8') && !lowerUrl.endsWith('.mpd')) {
      setValidationError('URL must end with .m3u8 (HLS) or .mpd (DASH)');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateUrl(url)) {
      return;
    }

    setIsLoading(true);
    onError(''); // Clear previous errors

    try {
      const { analyzeStream } = await import('../services/api');
      const result = await analyzeStream(url);
      onAnalyze(result);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred';
      onError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUrl(e.target.value);
    if (validationError) {
      setValidationError('');
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto px-6 py-8">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="stream-url" className="block text-sm font-medium text-gray-700 mb-2">
            Manifest URL
          </label>
          <input
            id="stream-url"
            type="text"
            value={url}
            onChange={handleUrlChange}
            placeholder="https://example.com/stream/manifest.m3u8 or .mpd"
            disabled={isLoading}
            className={`w-full px-4 py-3 text-base border rounded-lg shadow-sm transition-all
              focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none
              disabled:bg-gray-100 disabled:cursor-not-allowed
              ${validationError ? 'border-red-500' : 'border-gray-300'}`}
          />
          {validationError && (
            <p className="mt-2 text-sm text-red-600">{validationError}</p>
          )}
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full px-6 py-3 text-base font-medium text-white bg-blue-600 rounded-lg
            shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500
            focus:ring-offset-2 transition-all disabled:bg-gray-400 disabled:cursor-not-allowed
            disabled:hover:bg-gray-400"
        >
          {isLoading ? (
            <span className="flex items-center justify-center">
              <svg
                className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              Analyzing...
            </span>
          ) : (
            'View'
          )}
        </button>
      </form>
    </div>
  );
};

export default StreamAnalyzer;
