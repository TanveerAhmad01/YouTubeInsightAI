import React, { createContext, useContext, useState, ReactNode } from 'react';

// Define the shape of our results data
interface PerformanceData {
  loadTime: string;
  resourceCount: number;
  totalSize: string;
}

interface SeoData {
  title: boolean;
  description: boolean;
  headings: boolean;
  images: boolean;
}

interface MetaTags {
  [key: string]: string;
}

export interface UrlResultData {
  url: string;
  title: string;
  description: string;
  statusCode: number;
  contentType: string;
  server: string;
  securityScore: number;
  performance: PerformanceData;
  seo: SeoData;
  technologies: string[];
  metaTags: MetaTags;
}

interface UrlResultContextType {
  loading: boolean;
  results: UrlResultData | null;
  setLoading: (loading: boolean) => void;
  setResults: (results: UrlResultData | null) => void;
}

// Create context with default values
const UrlResultContext = createContext<UrlResultContextType>({
  loading: false,
  results: null,
  setLoading: () => {},
  setResults: () => {},
});

// Custom hook to use the context
export const useUrlResult = () => useContext(UrlResultContext);

// Provider component
export const UrlResultProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<UrlResultData | null>(null);

  return (
    <UrlResultContext.Provider value={{ loading, results, setLoading, setResults }}>
      {children}
    </UrlResultContext.Provider>
  );
};