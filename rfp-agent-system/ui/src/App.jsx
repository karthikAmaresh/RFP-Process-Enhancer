import { useState, useEffect } from 'react'
import Chat from './Chat'

function App() {
  const [file, setFile] = useState(null)
  const [isDragging, setIsDragging] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [progress, setProgress] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [showChat, setShowChat] = useState(false)
  const [showModal, setShowModal] = useState(false)
  const [documents, setDocuments] = useState([])
  const [selectedDocument, setSelectedDocument] = useState(null)
  const [isLoadingDocuments, setIsLoadingDocuments] = useState(true)
  const [workspaceName, setWorkspaceName] = useState('')
  const [workspaceDescription, setWorkspaceDescription] = useState('')

  // Fetch documents on component mount
  useEffect(() => {
    fetchDocuments()
  }, [])

  const fetchDocuments = async () => {
    setIsLoadingDocuments(true)
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/api/documents`)
      
      if (!response.ok) {
        throw new Error('Failed to fetch documents')
      }
      
      const data = await response.json()
      console.log('Fetched documents:', data)
      
      // Remove duplicates based on id
      const uniqueDocuments = Array.from(
        new Map(data.documents.map(doc => [doc.id, doc])).values()
      )
      
      console.log('Unique documents:', uniqueDocuments.length)
      setDocuments(uniqueDocuments)
    } catch (err) {
      console.error('Error fetching documents:', err)
      setDocuments([])
    } finally {
      setIsLoadingDocuments(false)
    }
  }

  const handleViewDocument = async (documentId) => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/api/documents/${documentId}`)
      
      if (!response.ok) {
        throw new Error('Failed to fetch document content')
      }
      
      const data = await response.json()
      setSelectedDocument(data)
    } catch (err) {
      console.error('Error fetching document:', err)
      alert('Failed to load document')
    }
  }

  const handleDownloadDocument = (documentId) => {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    window.open(`${apiUrl}/api/documents/${documentId}/download`, '_blank')
  }

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

      // Call backend API (Azure Functions or local)
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/api/process`, {
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
      
      // Refresh documents list after successful processing
      await fetchDocuments()
      
      // Reset form but keep modal open
      setFile(null)
      setWorkspaceName('')
      setWorkspaceDescription('')
      
    } catch (err) {
      setError('Failed to process document: ' + err.message)
    } finally {
      setIsProcessing(false)
      setProgress('')
    }
  }

  return (
    <div className="h-screen overflow-y-auto bg-gray-100 align-left">

      {/* Main Content */}
      <div className="container mx-auto px-0 py-8">
        <div className="bg-white rounded-lg shadow">
          {/* Workspace Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b bg-blue-600 text-white rounded-t-lg">
            <div>
              <h2 className="text-xl font-semibold">Smart Flow</h2>
              <p className="text-sm text-blue-100 mt-1">AI-Powered RFP Assistant</p>
            </div>
            <button
              onClick={() => setShowModal(true)}
              className="bg-white text-blue-600 px-4 py-2 rounded-md hover:bg-blue-50 transition-colors flex items-center gap-2 font-semibold"
            >
              <span className="text-xl">+</span> Create New
            </button>
          </div>

          {/* Documents Section */}
          <div className="px-6 py-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-700">
                Processed Documents ({documents.length})
              </h3>
              <button
                onClick={fetchDocuments}
                disabled={isLoadingDocuments}
                className="text-blue-600 hover:text-blue-800 flex items-center gap-1 text-sm"
              >
                <svg className={`w-4 h-4 ${isLoadingDocuments ? 'animate-spin' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Refresh
              </button>
            </div>

            {/* Loading State */}
            {isLoadingDocuments && documents.length === 0 && (
              <div className="text-center py-12">
                <div className="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
                <p className="text-gray-500">Loading documents...</p>
              </div>
            )}

            {/* Empty State */}
            {!isLoadingDocuments && documents.length === 0 && (
              <div className="text-center py-12">
                <svg className="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <p className="text-gray-500 text-lg mb-2">No documents yet</p>
                <p className="text-gray-400 text-sm">Upload an RFP document to get started</p>
              </div>
            )}

            {/* Documents Table */}
            {!isLoadingDocuments && documents.length > 0 && (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50 border-b">
                    <tr>
                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600">Workspace Name</th>
                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600">Size</th>
                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600">Modified</th>
                      <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {documents.map((doc) => (
                      <tr key={doc.id} className="border-b hover:bg-gray-50 transition-colors">
                        <td className="px-4 py-4">
                          <div className="flex items-center gap-2">
                            <svg className="w-5 h-5 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
                            </svg>
                            <span className="text-gray-700 font-medium">{doc.filename}</span>
                          </div>
                        </td>
                        <td className="px-4 py-4 text-gray-600 text-sm">{doc.size_formatted}</td>
                        <td className="px-4 py-4 text-gray-600 text-sm">
                          {new Date(doc.modified_at).toLocaleString()}
                        </td>
                        <td className="px-4 py-4">
                          <div className="flex gap-2">
                            <button
                              onClick={() => handleViewDocument(doc.id)}
                              className="text-blue-600 hover:text-blue-800 p-1 hover:bg-blue-50 rounded transition-colors"
                              title="View Document"
                            >
                              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                              </svg>
                            </button>
                            <button
                              onClick={() => handleDownloadDocument(doc.id)}
                              className="text-green-600 hover:text-green-800 p-1 hover:bg-green-50 rounded transition-colors"
                              title="Download Document"
                            >
                              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                              </svg>
                            </button>
                            <button
                              onClick={() => setShowChat(true)}
                              className="text-purple-600 hover:text-purple-800 p-1 hover:bg-purple-50 rounded transition-colors"
                              title="Chat with Document"
                            >
                              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M2 5a2 2 0 012-2h7a2 2 0 012 2v4a2 2 0 01-2 2H9l-3 3v-3H4a2 2 0 01-2-2V5z" />
                                <path d="M15 7v2a4 4 0 01-4 4H9.828l-1.766 1.767c.28.149.599.233.938.233h2l3 3v-3h2a2 2 0 002-2V9a2 2 0 00-2-2h-1z" />
                              </svg>
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Document Viewer Modal */}
      {selectedDocument && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] flex flex-col">
            <div className="flex items-center justify-between px-8 py-6 border-b">
              <h2 className="text-2xl font-bold text-blue-900">{selectedDocument.filename}</h2>
              <button
                onClick={() => setSelectedDocument(null)}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="p-8 overflow-y-auto flex-1">
              <pre className="whitespace-pre-wrap text-sm text-gray-700 font-mono bg-gray-50 p-6 rounded-lg border">
                {selectedDocument.content}
              </pre>
            </div>
            <div className="px-8 py-4 border-t bg-gray-50 rounded-b-2xl flex gap-3 justify-end">
              <button
                onClick={() => handleDownloadDocument(selectedDocument.document_id)}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                Download
              </button>
              <button
                onClick={() => setSelectedDocument(null)}
                className="bg-gray-200 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-300 transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Upload Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between px-8 py-6 border-b">
              <h2 className="text-2xl font-bold text-blue-900">Upload RFP Document</h2>
              <button
                onClick={() => {
                  setShowModal(false)
                  setFile(null)
                  setError(null)
                  setWorkspaceName('')
                  setWorkspaceDescription('')
                }}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="p-8">
              {/* Workspace Name Input */}
              {!result && <div className="mb-6">
                <label htmlFor="workspaceName" className="block text-sm font-semibold text-gray-700 mb-2">
                  Workspace Name
                </label>
                <input
                  type="text"
                  id="workspaceName"
                  value={workspaceName}
                  onChange={(e) => setWorkspaceName(e.target.value)}
                  placeholder="Enter workspace name (e.g., Customer Support RFP)"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
                />
              </div>}

              {/* Workspace Description Input */}
              {!result && <div className="mb-6">
                <label htmlFor="workspaceDescription" className="block text-sm font-semibold text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  id="workspaceDescription"
                  value={workspaceDescription}
                  onChange={(e) => setWorkspaceDescription(e.target.value)}
                  placeholder="Enter a brief description of this workspace"
                  rows="3"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all resize-none"
                />
              </div>}

              {/* File Upload Area */}
              {!result && <div
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
              </div>}

              {error && (
                <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                  {error}
                </div>
              )}

              {isProcessing && (
                <div className="mt-6 p-6 bg-blue-50 rounded-xl text-center">
                  <div className="flex flex-col items-center">
                    <div className="w-12 h-12 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin mb-4"></div>
                    <p className="text-lg text-indigo-600 font-semibold animate-pulse">
                      {progress || 'Processing your document...'}
                    </p>
                  </div>
                </div>
              )}

              {file && !error && !isProcessing && (
                <div className="mt-6 flex justify-center">
                  <button
                    onClick={handleUpload}
                    disabled={!workspaceName.trim()}
                    className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-8 py-4 rounded-xl font-bold text-lg hover:from-indigo-700 hover:to-purple-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                  >
                    Process Document
                  </button>
                </div>
              )}

              {/* Results Section */}
              {result && (
                <div className="mt-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-2xl font-bold text-gray-900">
                      Analysis Complete
                    </h3>
                    <button
                      onClick={() => {
                        setFile(null)
                        setResult(null)
                        setWorkspaceName('')
                        setWorkspaceDescription('')
                      }}
                      className="bg-gray-200 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-300 transition-colors"
                    >
                      Process Another
                    </button>
                  </div>
                  
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
                    <p className="text-green-800 font-semibold">{result.message}</p>
                  </div>

                  <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                    <div className="flex items-center justify-between mb-4">
                      <h4 className="text-lg font-semibold text-gray-900">Knowledge Base</h4>
                      <div className="flex gap-2">
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
                        <button
                          onClick={() => setShowChat(true)}
                          className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors flex items-center gap-2"
                        >
                          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M2 5a2 2 0 012-2h7a2 2 0 012 2v4a2 2 0 01-2 2H9l-3 3v-3H4a2 2 0 01-2-2V5z" />
                            <path d="M15 7v2a4 4 0 01-4 4H9.828l-1.766 1.767c.28.149.599.233.938.233h2l3 3v-3h2a2 2 0 002-2V9a2 2 0 00-2-2h-1z" />
                          </svg>
                          Chat
                        </button>
                      </div>
                    </div>
                    <div className="text-gray-700 whitespace-pre-wrap overflow-auto max-h-96 text-sm font-mono bg-white p-4 rounded border border-gray-300">
                      {result.output}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Chat Modal */}
      {showChat && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full h-[80vh] flex flex-col">
            <div className="flex items-center justify-between px-8 py-6 border-b">
              <h2 className="text-2xl font-bold text-blue-900">Chat with Knowledge Base</h2>
              <button
                onClick={() => setShowChat(false)}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="flex-1 overflow-hidden">
              <Chat />
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="bg-[#1e2875] text-white py-4 mt-auto fixed bottom-0 w-full">
        <div className="container mx-auto px-4 text-center text-sm">
          © 2025 RFP Process Enhancer. All rights reserved.
        </div>
      </footer>
    </div>
  )
}

export default App
