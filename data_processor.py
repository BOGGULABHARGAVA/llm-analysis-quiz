"""
Data processing utilities for handling various file formats and data analysis
"""
import io
import logging
import os
import tempfile
from typing import Any, Dict, List, Optional, Union
import requests
import pandas as pd
import numpy as np
from PIL import Image
import PyPDF2
import base64
import json

logger = logging.getLogger(__name__)


class DataProcessor:
    """Handles data processing for various file formats"""
    
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
    
    def download_file(self, url: str, max_size: int = 10 * 1024 * 1024) -> Optional[bytes]:
        """
        Download a file from URL
        
        Args:
            url: File URL
            max_size: Maximum file size in bytes (default 10MB)
            
        Returns:
            File content as bytes or None if failed
        """
        try:
            logger.info(f"Downloading file from: {url}")
            
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Check content length
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > max_size:
                logger.error(f"File too large: {content_length} bytes")
                return None
            
            # Download with size limit
            content = b''
            for chunk in response.iter_content(chunk_size=8192):
                content += chunk
                if len(content) > max_size:
                    logger.error("File exceeded size limit during download")
                    return None
            
            logger.info(f"Downloaded {len(content)} bytes")
            return content
            
        except Exception as e:
            logger.error(f"Error downloading file: {e}")
            return None
    
    def read_pdf(self, content: bytes) -> Optional[str]:
        """
        Extract text from PDF
        
        Args:
            content: PDF file content as bytes
            
        Returns:
            Extracted text or None
        """
        try:
            pdf_file = io.BytesIO(content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += f"\n--- Page {page_num + 1} ---\n"
                text += page.extract_text()
            
            logger.info(f"Extracted {len(text)} chars from PDF")
            return text
            
        except Exception as e:
            logger.error(f"Error reading PDF: {e}")
            return None
    
    def read_csv(self, content: bytes, **kwargs) -> Optional[pd.DataFrame]:
        """
        Read CSV file into DataFrame
        
        Args:
            content: CSV file content as bytes
            **kwargs: Additional arguments for pandas.read_csv
            
        Returns:
            DataFrame or None
        """
        try:
            df = pd.read_csv(io.BytesIO(content), **kwargs)
            logger.info(f"Read CSV: {df.shape[0]} rows, {df.shape[1]} columns")
            return df
            
        except Exception as e:
            logger.error(f"Error reading CSV: {e}")
            return None
    
    def read_excel(self, content: bytes, **kwargs) -> Optional[pd.DataFrame]:
        """
        Read Excel file into DataFrame
        
        Args:
            content: Excel file content as bytes
            **kwargs: Additional arguments for pandas.read_excel
            
        Returns:
            DataFrame or None
        """
        try:
            df = pd.read_excel(io.BytesIO(content), **kwargs)
            logger.info(f"Read Excel: {df.shape[0]} rows, {df.shape[1]} columns")
            return df
            
        except Exception as e:
            logger.error(f"Error reading Excel: {e}")
            return None
    
    def read_json(self, content: bytes) -> Optional[Union[Dict, List]]:
        """
        Parse JSON content
        
        Args:
            content: JSON content as bytes
            
        Returns:
            Parsed JSON data or None
        """
        try:
            data = json.loads(content.decode('utf-8'))
            logger.info(f"Parsed JSON data")
            return data
            
        except Exception as e:
            logger.error(f"Error reading JSON: {e}")
            return None
    
    def read_image(self, content: bytes) -> Optional[Image.Image]:
        """
        Load image from bytes
        
        Args:
            content: Image content as bytes
            
        Returns:
            PIL Image or None
        """
        try:
            image = Image.open(io.BytesIO(content))
            logger.info(f"Loaded image: {image.size}, {image.mode}")
            return image
            
        except Exception as e:
            logger.error(f"Error reading image: {e}")
            return None
    
    def dataframe_to_dict(self, df: pd.DataFrame, orient: str = 'records') -> List[Dict]:
        """Convert DataFrame to list of dictionaries"""
        try:
            return df.to_dict(orient=orient)
        except Exception as e:
            logger.error(f"Error converting DataFrame: {e}")
            return []
    
    def analyze_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get basic statistics and info about a DataFrame
        
        Returns:
            Dictionary with analysis results
        """
        try:
            analysis = {
                'shape': df.shape,
                'columns': df.columns.tolist(),
                'dtypes': df.dtypes.astype(str).to_dict(),
                'null_counts': df.isnull().sum().to_dict(),
                'numeric_stats': {},
                'sample_rows': df.head(3).to_dict(orient='records')
            }
            
            # Get stats for numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                analysis['numeric_stats'][col] = {
                    'mean': float(df[col].mean()),
                    'median': float(df[col].median()),
                    'std': float(df[col].std()),
                    'min': float(df[col].min()),
                    'max': float(df[col].max()),
                    'sum': float(df[col].sum())
                }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing DataFrame: {e}")
            return {}
    
    def create_visualization(self, df: pd.DataFrame, viz_type: str = 'bar', 
                           x: str = None, y: str = None) -> Optional[bytes]:
        """
        Create a simple visualization and return as PNG bytes
        
        Args:
            df: DataFrame to visualize
            viz_type: Type of visualization (bar, line, scatter, hist)
            x: Column for x-axis
            y: Column for y-axis
            
        Returns:
            PNG image as bytes or None
        """
        try:
            import matplotlib
            matplotlib.use('Agg')  # Non-interactive backend
            import matplotlib.pyplot as plt
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            if viz_type == 'bar' and x and y:
                df.plot(kind='bar', x=x, y=y, ax=ax)
            elif viz_type == 'line' and x and y:
                df.plot(kind='line', x=x, y=y, ax=ax)
            elif viz_type == 'scatter' and x and y:
                df.plot(kind='scatter', x=x, y=y, ax=ax)
            elif viz_type == 'hist' and x:
                df[x].plot(kind='hist', ax=ax)
            else:
                # Default: just plot the dataframe
                df.plot(ax=ax)
            
            plt.tight_layout()
            
            # Save to bytes
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=100)
            plt.close(fig)
            
            buf.seek(0)
            image_bytes = buf.read()
            
            logger.info(f"Created visualization: {len(image_bytes)} bytes")
            return image_bytes
            
        except Exception as e:
            logger.error(f"Error creating visualization: {e}")
            return None
    
    def image_to_base64(self, image_bytes: bytes, mime_type: str = 'image/png') -> str:
        """Convert image bytes to base64 data URI"""
        try:
            b64 = base64.b64encode(image_bytes).decode('utf-8')
            return f"data:{mime_type};base64,{b64}"
        except Exception as e:
            logger.error(f"Error encoding image: {e}")
            return ""
