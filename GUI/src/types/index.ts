// This file contains type definitions that might be used across the application

// Types for Flask API integration
export interface FlaskUrlAnalysisRequest {
  url: string;
}

export interface FlaskUrlAnalysisResponse {
  success: boolean;
  data?: any;
  error?: string;
}

// Additional utility types can be added here as needed