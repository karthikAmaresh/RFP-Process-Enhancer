import { useState } from 'react'

function App() {
  const [file, setFile] = useState(null)
  const [isDragging, setIsDragging] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [progress, setProgress] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    const droppedFile = e.dataTransfer.files[0]
    if (droppedFile && droppedFile.type === 'application/pdf') {
      setFile(droppedFile)
      setError(null)
    } else {
      setError('Please upload a PDF file')
    }
  }

  const handleFileInput = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile)
      setError(null)
    } else {
      setError('Please upload a PDF file')
    }
  }

  const handleUpload = async () => {
    if (!file) return

    setIsProcessing(true)
    setError(null)
    setResult(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      // Show progress updates
      const steps = [
        'Uploading document...',
        'Extracting text from PDF...',
        'Chunking document...',
        'Creating embeddings...',
        'Running AI agents...',
        'Generating analysis...'
      ]

      let stepIndex = 0
      const progressInterval = setInterval(() => {
        if (stepIndex < steps.length) {
          setProgress(steps[stepIndex])
          stepIndex++
        }
      }, 3000)

      // Call backend API
      const response = await fetch('http://localhost:8000/api/process', {
        method: 'POST',
        body: formData
      })

      clearInterval(progressInterval)

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Processing failed')
      }

      const data = await response.json()
      
      setResult({
        message: data.message,
        output: data.output
      })
      
    } catch (err) {
      setError('Failed to process document: ' + err.message)
    } finally {
      setIsProcessing(false)
      setProgress('')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-gray-900 mb-4">
              RFP Process Enhancer
            </h1>
            <p className="text-xl text-gray-600">
              Upload your RFP document to get AI-powered analysis and insights
            </p>
          </div>

          {/* Upload Section */}
          {!isProcessing && !result && (
            <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
              <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={`border-3 border-dashed rounded-xl p-12 text-center transition-all duration-300 ${
                  isDragging
                    ? 'border-indigo-500 bg-indigo-50 scale-105'
                    : 'border-gray-300 hover:border-indigo-400 hover:bg-gray-50'
                }`}
              >
                <svg
                  className="mx-auto h-16 w-16 text-gray-400 mb-4"
                  stroke="currentColor"
                  fill="none"
                  viewBox="0 0 48 48"
                >
                  <path
                    d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                    strokeWidth={2}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
                <p className="text-xl font-semibold text-gray-700 mb-2">
                  {file ? file.name : 'Drop your PDF here'}
                </p>
                <p className="text-sm text-gray-500 mb-4">or click to browse</p>
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileInput}
                  className="hidden"
                  id="fileInput"
                />
                <label
                  htmlFor="fileInput"
                  className="inline-block bg-indigo-600 text-white px-6 py-3 rounded-lg font-semibold cursor-pointer hover:bg-indigo-700 transition-colors"
                >
                  Select PDF
                </label>
              </div>

              {error && (
                <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                  {error}
                </div>
              )}

              {file && !error && (
                <div className="mt-6 flex justify-center">
                  <button
                    onClick={handleUpload}
                    className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-8 py-4 rounded-xl font-bold text-lg hover:from-indigo-700 hover:to-purple-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
                  >
                    Process Document
                  </button>
                </div>
              )}
            </div>
          )}

          {/* Processing State */}
          {isProcessing && (
            <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
              <div className="flex flex-col items-center">
                <div className="relative">
                  <div className="w-24 h-24 border-8 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="w-16 h-16 bg-indigo-100 rounded-full"></div>
                  </div>
                </div>
                <h2 className="text-2xl font-bold text-gray-900 mt-8 mb-4">
                  Processing Your Document
                </h2>
                <p className="text-lg text-indigo-600 font-semibold animate-pulse">
                  {progress}
                </p>
                <p className="text-sm text-gray-500 mt-4">
                  This may take a few minutes...
                </p>
              </div>
            </div>
          )}

          {/* Results Section */}
          {result && (
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-3xl font-bold text-gray-900">
                  Analysis Complete
                </h2>
                <button
                  onClick={() => {
                    setFile(null)
                    setResult(null)
                  }}
                  className="bg-gray-200 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-300 transition-colors"
                >
                  Process Another
                </button>
              </div>
              
              <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
                <p className="text-green-800 font-semibold">{result.message}</p>
              </div>

              <div className="prose max-w-none">
                <div className="bg-gray-50 rounded-lg p-6 border border-gray-200">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-semibold text-gray-900">Knowledge Base</h3>
                    <button
                      onClick={() => {
                        const blob = new Blob([result.output], { type: 'text/markdown' })
                        const url = URL.createObjectURL(blob)
                        const a = document.createElement('a')
                        a.href = url
                        a.download = 'knowledge-base.md'
                        a.click()
                        URL.revokeObjectURL(url)
                      }}
                      className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors flex items-center gap-2"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                      </svg>
                      Download KB
                    </button>
                  </div>
                  <div className="text-gray-700 whitespace-pre-wrap overflow-auto max-h-96 text-sm font-mono bg-white p-4 rounded border border-gray-300">
                    {result.output}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
