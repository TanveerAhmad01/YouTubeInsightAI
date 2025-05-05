import React, { useState } from 'react';
import { Search, Link as LinkIcon } from 'lucide-react';
import { useUrlResult } from '../context/UrlResultContext';

const UrlForm: React.FC = () => {
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');
  const { setLoading, setResults } = useUrlResult();

  const validateUrl = (input: string): boolean => {
    try {
      new URL(input);
      return true;
    } catch (err) {
      return false;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Basic URL validation
    if (!url.trim()) {
      setError('Please enter a URL');
      return;
    }

    // Add http if missing
    let processedUrl = url;
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      processedUrl = 'https://' + url;
    }

    if (!validateUrl(processedUrl)) {
      setError('Please enter a valid URL');
      return;
    }

    // Show loading state
    setLoading(true);
    
    try {
      // This would be your Flask API endpoint
      // For demo purposes, we'll simulate a response
      setTimeout(() => {
        // Mock response - in real app, this would be from your Flask backend
        setResults({
          url: processedUrl,
          title: 'Example Website',
          description: 'This is a sample description of the analyzed website.',
          statusCode: 200,
          contentType: 'text/html',
          server: 'nginx/1.14.2',
          securityScore: 87,
          performance: {
            loadTime: '1.2s',
            resourceCount: 45,
            totalSize: '1.4 MB'
          },
          seo: {
            title: true,
            description: true,
            headings: true,
            images: false
          },
          technologies: ['React', 'Tailwind CSS', 'Node.js'],
          metaTags: {
            author: 'John Doe',
            keywords: 'web, development, design',
            viewport: 'width=device-width, initial-scale=1.0'
          }
        });
        setLoading(false);
      }, 1500);
    } catch (err) {
      console.error('Error analyzing URL:', err);
      setError('An error occurred while analyzing the URL');
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 transition-all duration-300 hover:shadow-xl w-full">
      <form onSubmit={handleSubmit} className="relative">
        <div className="flex flex-col md:flex-row items-stretch md:items-center gap-4">
          <div className="relative flex-grow group">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <LinkIcon className="h-5 w-5 text-slate-400 group-focus-within:text-blue-900 transition-colors" />
            </div>
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Enter website URL (e.g., example.com)"
              className="w-full py-3 pl-10 pr-4 rounded-lg border border-slate-300 focus:border-blue-900 focus:ring-2 focus:ring-blue-900/20 focus:outline-none transition-all duration-200"
            />
          </div>
          <button
            type="submit"
            className="bg-blue-900 hover:bg-blue-800 text-white font-medium py-3 px-6 rounded-lg transition-all duration-200 flex items-center justify-center"
          >
            <Search className="h-5 w-5 mr-2" />
            Analyze
          </button>
        </div>
        
        {error && (
          <p className="mt-2 text-red-600 text-sm">{error}</p>
        )}
      </form>
    </div>
  );
};

export default UrlForm;