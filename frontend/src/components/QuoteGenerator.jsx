import React, { useState } from 'react';
import axios from 'axios';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from './ui/card';
import { Loader2, Quote, Shuffle, Copy, Check } from 'lucide-react';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const API = `${API_BASE}/api`;

const QuoteGenerator = () => {
  const [theme, setTheme] = useState('');
  const [quotes, setQuotes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [copiedIndex, setCopiedIndex] = useState(null);

  const popularThemes = [
    'Success', 'Motivation', 'Love', 'Friendship', 'Perseverance',
    'Happiness', 'Wisdom', 'Leadership', 'Innovation', 'Dreams',
    'Life', 'Courage', 'Hope', 'Change', 'Growth'
  ];

  const generateQuotes = async (selectedTheme = theme, count = 3) => {
    if (!selectedTheme.trim()) {
      setError('Please enter a theme');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API}/quotes/generate`, {
        theme: selectedTheme,
        count: count
      });

      if (response.data.success) {
        setQuotes(response.data.quotes);
        setTheme(selectedTheme);
      } else {
        setError(response.data.error || 'Failed to generate quotes');
      }
    } catch (err) {
      setError('Error connecting to the server. Please try again.');
      console.error('Quote generation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = async (text, index) => {
    try {
      await navigator.clipboard.writeText(`"${text}"`);
      setCopiedIndex(index);
      setTimeout(() => setCopiedIndex(null), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  const handleThemeClick = (selectedTheme) => {
    setTheme(selectedTheme);
    generateQuotes(selectedTheme, 3);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-100 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 mb-4">
            <Quote className="w-8 h-8 text-purple-600" />
            <h1 className="text-4xl font-bold text-gray-800">Quote Generator</h1>
          </div>
          <p className="text-gray-600 text-lg">Generate inspiring quotes based on any theme</p>
        </div>

        {/* Theme Input Section */}
        <Card className="mb-8 shadow-lg">
          <CardHeader>
            <CardTitle className="text-xl text-gray-800">Choose Your Theme</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex gap-2">
              <Input
                type="text"
                placeholder="Enter a theme (e.g., motivation, love, success...)"
                value={theme}
                onChange={(e) => setTheme(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && generateQuotes()}
                className="flex-1"
              />
              <Button
                onClick={() => generateQuotes()}
                disabled={loading || !theme.trim()}
                className="min-w-[120px]"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin mr-2" />
                    Generating...
                  </>
                ) : (
                  <>
                    <Shuffle className="w-4 h-4 mr-2" />
                    Generate
                  </>
                )}
              </Button>
            </div>

            {/* Popular Themes */}
            <div>
              <p className="text-sm text-gray-600 mb-3">Or choose a popular theme:</p>
              <div className="flex flex-wrap gap-2">
                {popularThemes.map((popularTheme) => (
                  <Button
                    key={popularTheme}
                    variant="outline"
                    size="sm"
                    onClick={() => handleThemeClick(popularTheme)}
                    disabled={loading}
                    className="text-xs"
                  >
                    {popularTheme}
                  </Button>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Error Display */}
        {error && (
          <Card className="mb-8 border-red-200 bg-red-50">
            <CardContent className="pt-6">
              <p className="text-red-600 text-center">{error}</p>
            </CardContent>
          </Card>
        )}

        {/* Quotes Display */}
        {quotes.length > 0 && (
          <div className="space-y-6">
            <h2 className="text-2xl font-semibold text-gray-800 text-center mb-6">
              Quotes about "{theme}"
            </h2>

            <div className="grid gap-6 md:grid-cols-1 lg:grid-cols-1">
              {quotes.map((quote, index) => (
                <Card key={index} className="shadow-lg hover:shadow-xl transition-shadow duration-300 border-l-4 border-l-purple-500">
                  <CardContent className="pt-6">
                    <div className="flex items-start gap-4">
                      <Quote className="w-8 h-8 text-purple-500 flex-shrink-0 mt-1" />
                      <div className="flex-1">
                        <blockquote className="text-lg text-gray-700 font-medium leading-relaxed mb-4">
                          "{quote.text}"
                        </blockquote>
                        <div className="flex items-center justify-between">
                          <p className="text-purple-600 font-semibold">
                            — {quote.author}
                          </p>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => copyToClipboard(quote.text, index)}
                            className="text-gray-500 hover:text-purple-600"
                          >
                            {copiedIndex === index ? (
                              <>
                                <Check className="w-4 h-4 mr-1" />
                                Copied!
                              </>
                            ) : (
                              <>
                                <Copy className="w-4 h-4 mr-1" />
                                Copy
                              </>
                            )}
                          </Button>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Generate More Button */}
            <div className="text-center">
              <Button
                onClick={() => generateQuotes(theme, 3)}
                disabled={loading}
                variant="outline"
                className="min-w-[160px]"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin mr-2" />
                    Generating...
                  </>
                ) : (
                  <>
                    <Shuffle className="w-4 h-4 mr-2" />
                    Generate More
                  </>
                )}
              </Button>
            </div>
          </div>
        )}

        {/* Empty State */}
        {quotes.length === 0 && !loading && !error && (
          <Card className="text-center py-12 shadow-lg">
            <CardContent>
              <Quote className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-600 mb-2">
                Ready to Generate Quotes?
              </h3>
              <p className="text-gray-500">
                Enter a theme above or choose from popular themes to get started
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default QuoteGenerator;