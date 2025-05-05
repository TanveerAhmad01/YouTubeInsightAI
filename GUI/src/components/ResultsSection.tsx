import React from 'react';
import { 
  Loader2, 
  CheckCircle, 
  XCircle, 
  Server, 
  Shield, 
  Zap,
  Search,
  Code,
  Tag,
  Copy,
  Download
} from 'lucide-react';
import { useUrlResult } from '../context/UrlResultContext';

const ResultsSection: React.FC = () => {
  const { loading, results } = useUrlResult();

  if (loading) {
    return (
      <div className="w-full max-w-3xl mx-auto mt-8 flex flex-col items-center justify-center p-12 bg-white rounded-xl shadow-lg">
        <Loader2 className="h-12 w-12 text-blue-900 animate-spin" />
        <p className="mt-4 text-lg text-slate-700">Analyzing URL...</p>
      </div>
    );
  }

  if (!results) {
    return null;
  }

  return (
    <div className="w-full max-w-3xl mx-auto mt-4 mb-8 opacity-100 animate-fadeIn">
      <div className="flex justify-between mb-6">
        <h2 className="text-2xl font-bold text-slate-800">Analysis Results</h2>
        <div className="flex gap-2">
          <button className="flex items-center text-sm bg-white border border-slate-300 hover:bg-slate-50 px-3 py-1.5 rounded-md">
            <Copy className="h-4 w-4 mr-1" />
            Copy
          </button>
          <button className="flex items-center text-sm bg-white border border-slate-300 hover:bg-slate-50 px-3 py-1.5 rounded-md">
            <Download className="h-4 w-4 mr-1" />
            Export
          </button>
        </div>
      </div>
      
      {/* Overview Card */}
      <div className="bg-white rounded-xl shadow p-6 mb-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between mb-4">
          <div>
            <h3 className="text-xl font-semibold mb-1">{results.title}</h3>
            <a 
              href={results.url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-blue-900 hover:underline text-sm inline-flex items-center"
            >
              {results.url}
              <LinkArrow className="ml-1 h-3 w-3" />
            </a>
          </div>
          <div className="mt-3 md:mt-0 bg-green-100 px-3 py-1 rounded-full text-sm text-green-800 font-medium inline-flex items-center">
            <CheckCircle className="h-4 w-4 mr-1" />
            Status: {results.statusCode} OK
          </div>
        </div>
        <p className="text-slate-600">{results.description}</p>
      </div>
      
      {/* Technical Details Card */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-xl shadow p-6">
          <div className="flex items-center mb-4">
            <Server className="h-5 w-5 text-blue-900 mr-2" />
            <h3 className="text-lg font-semibold">Server Information</h3>
          </div>
          <ul className="space-y-3">
            <li className="flex justify-between">
              <span className="text-slate-600">Content Type:</span>
              <span className="font-medium">{results.contentType}</span>
            </li>
            <li className="flex justify-between">
              <span className="text-slate-600">Server:</span>
              <span className="font-medium">{results.server}</span>
            </li>
          </ul>
        </div>
        
        <div className="bg-white rounded-xl shadow p-6">
          <div className="flex items-center mb-4">
            <Shield className="h-5 w-5 text-blue-900 mr-2" />
            <h3 className="text-lg font-semibold">Security</h3>
          </div>
          <div className="flex flex-col items-center">
            <div className="relative mb-2">
              <svg className="w-24 h-24">
                <circle 
                  className="text-slate-200" 
                  strokeWidth="6" 
                  stroke="currentColor" 
                  fill="transparent" 
                  r="36" 
                  cx="42" 
                  cy="42"
                />
                <circle 
                  className="text-blue-900" 
                  strokeWidth="6" 
                  strokeLinecap="round" 
                  stroke="currentColor" 
                  fill="transparent" 
                  r="36" 
                  cx="42" 
                  cy="42" 
                  strokeDasharray="226.1" 
                  strokeDashoffset={(1 - results.securityScore / 100) * 226.1}
                />
              </svg>
              <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-xl font-bold text-blue-900">
                {results.securityScore}
              </div>
            </div>
            <span className="text-slate-600 text-sm">Security Score</span>
          </div>
        </div>
      </div>
      
      {/* Performance Card */}
      <div className="bg-white rounded-xl shadow p-6 mb-6">
        <div className="flex items-center mb-4">
          <Zap className="h-5 w-5 text-blue-900 mr-2" />
          <h3 className="text-lg font-semibold">Performance</h3>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="bg-slate-50 p-4 rounded-lg text-center">
            <div className="text-xl font-semibold">{results.performance.loadTime}</div>
            <div className="text-sm text-slate-600">Load Time</div>
          </div>
          <div className="bg-slate-50 p-4 rounded-lg text-center">
            <div className="text-xl font-semibold">{results.performance.resourceCount}</div>
            <div className="text-sm text-slate-600">Resources</div>
          </div>
          <div className="bg-slate-50 p-4 rounded-lg text-center">
            <div className="text-xl font-semibold">{results.performance.totalSize}</div>
            <div className="text-sm text-slate-600">Total Size</div>
          </div>
        </div>
      </div>
      
      {/* SEO Card */}
      <div className="bg-white rounded-xl shadow p-6 mb-6">
        <div className="flex items-center mb-4">
          <Search className="h-5 w-5 text-blue-900 mr-2" />
          <h3 className="text-lg font-semibold">SEO Analysis</h3>
        </div>
        <ul className="space-y-3">
          <li className="flex items-center">
            {results.seo.title 
              ? <CheckCircle className="h-5 w-5 text-green-500 mr-2" /> 
              : <XCircle className="h-5 w-5 text-red-500 mr-2" />
            }
            <span>Title tag is {results.seo.title ? 'properly' : 'not properly'} defined</span>
          </li>
          <li className="flex items-center">
            {results.seo.description 
              ? <CheckCircle className="h-5 w-5 text-green-500 mr-2" /> 
              : <XCircle className="h-5 w-5 text-red-500 mr-2" />
            }
            <span>Meta description is {results.seo.description ? 'properly' : 'not properly'} defined</span>
          </li>
          <li className="flex items-center">
            {results.seo.headings 
              ? <CheckCircle className="h-5 w-5 text-green-500 mr-2" /> 
              : <XCircle className="h-5 w-5 text-red-500 mr-2" />
            }
            <span>Heading structure is {results.seo.headings ? 'properly' : 'not properly'} implemented</span>
          </li>
          <li className="flex items-center">
            {results.seo.images 
              ? <CheckCircle className="h-5 w-5 text-green-500 mr-2" /> 
              : <XCircle className="h-5 w-5 text-red-500 mr-2" />
            }
            <span>Images {results.seo.images ? 'have' : 'are missing'} alt attributes</span>
          </li>
        </ul>
      </div>
      
      {/* Technologies and Meta Tags */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow p-6">
          <div className="flex items-center mb-4">
            <Code className="h-5 w-5 text-blue-900 mr-2" />
            <h3 className="text-lg font-semibold">Technologies</h3>
          </div>
          <div className="flex flex-wrap gap-2">
            {results.technologies.map((tech, index) => (
              <span key={index} className="bg-slate-100 text-slate-800 px-3 py-1 rounded-full text-sm">
                {tech}
              </span>
            ))}
          </div>
        </div>
        
        <div className="bg-white rounded-xl shadow p-6">
          <div className="flex items-center mb-4">
            <Tag className="h-5 w-5 text-blue-900 mr-2" />
            <h3 className="text-lg font-semibold">Meta Tags</h3>
          </div>
          <ul className="space-y-2 text-sm">
            {Object.entries(results.metaTags).map(([key, value]) => (
              <li key={key} className="flex flex-col">
                <span className="font-medium text-slate-700">{key}:</span>
                <span className="text-slate-600">{value}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

// Custom arrow icon for external links
const LinkArrow = ({ className }: { className?: string }) => (
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    viewBox="0 0 20 20" 
    fill="currentColor" 
    className={className}
  >
    <path 
      fillRule="evenodd" 
      d="M5.22 14.78a.75.75 0 001.06 0l7.22-7.22v5.69a.75.75 0 001.5 0v-7.5a.75.75 0 00-.75-.75h-7.5a.75.75 0 000 1.5h5.69l-7.22 7.22a.75.75 0 000 1.06z" 
      clipRule="evenodd" 
    />
  </svg>
);

export default ResultsSection;