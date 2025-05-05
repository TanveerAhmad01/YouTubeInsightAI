import React from 'react';
import { ChevronsDown } from 'lucide-react';
import Header from './components/Header';
import Footer from './components/Footer';
import UrlForm from './components/UrlForm';
import ResultsSection from './components/ResultsSection';
import { UrlResultProvider } from './context/UrlResultContext';

function App() {
  return (
    <UrlResultProvider>
      <div className="min-h-screen flex flex-col bg-gradient-to-br from-slate-50 to-slate-100 text-slate-800">
        <Header />
        
        <main className="flex-grow flex flex-col items-center justify-start w-full px-4 py-8 md:py-12">
          <section className="w-full max-w-3xl mx-auto text-center mb-8 md:mb-12">
            <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-900 to-teal-600">
              URL Analyzer
            </h1>
            <p className="text-lg md:text-xl text-slate-600 mb-8">
              Enter any URL to analyze and get comprehensive insights
            </p>
            
            <UrlForm />
            
            <div className="mt-12 animate-bounce">
              <ChevronsDown className="mx-auto text-slate-400" size={28} />
            </div>
          </section>
          
          <ResultsSection />
        </main>
        
        <Footer />
      </div>
    </UrlResultProvider>
  );
}

export default App;