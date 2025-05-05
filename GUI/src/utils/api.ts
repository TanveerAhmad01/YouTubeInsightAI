/**
 * API utilities for communicating with the Flask backend
 */

// Base URL for Flask API - configured from environment or defaults to localhost
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

/**
 * Send a URL for analysis to the Flask backend
 * @param url - The URL to analyze
 * @returns Promise with the analysis results
 */
export const analyzeUrl = async (url: string) => {
  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to analyze URL');
    }
    
    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
};

/**
 * Fetch analysis history from the Flask backend
 * @returns Promise with the analysis history
 */
export const getAnalysisHistory = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/history`);
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to fetch history');
    }
    
    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
};