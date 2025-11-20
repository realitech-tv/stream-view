import { useState } from 'react';
import Header from './components/Header';
import StreamAnalyzer from './components/StreamAnalyzer';
import ErrorMessage from './components/ErrorMessage';
import ResultsDisplay from './components/ResultsDisplay';
import type { AnalyzeResponse } from './types/api';

function App() {
  const [results, setResults] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState<string>('');

  const handleAnalyze = (data: AnalyzeResponse) => {
    setResults(data);
    setError('');
  };

  const handleError = (errorMessage: string) => {
    setError(errorMessage);
    setResults(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="py-8">
        <StreamAnalyzer onAnalyze={handleAnalyze} onError={handleError} />

        {error && (
          <div className="mt-6">
            <ErrorMessage message={error} />
          </div>
        )}

        {results && (
          <div className="mt-8">
            <ResultsDisplay data={results} />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
