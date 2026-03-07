import { useEffect, useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { documentsAPI } from '../services/api'
import toast from 'react-hot-toast'
import { FiUpload, FiFileText, FiTrash2, FiCheck, FiLoader } from 'react-icons/fi'
import { motion, AnimatePresence } from 'framer-motion'

interface Document {
  id: number
  title: string
  file_name: string
  file_type: string
  file_size: number
  status: string
  chunk_count: number
  created_at: string
}

export default function Documents() {
  const [documents, setDocuments] = useState<Document[]>([])
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)

  useEffect(() => {
    loadDocuments()
  }, [])

  const loadDocuments = async () => {
    try {
      const response = await documentsAPI.list()
      setDocuments(response.data)
    } catch (error) {
      console.error('Failed to load documents')
    } finally {
      setLoading(false)
    }
  }

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    for (const file of acceptedFiles) {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('title', file.name.replace(/\.[^/.]+$/, ''))
      
      setUploading(true)
      try {
        const response = await documentsAPI.upload(formData)
        setDocuments(prev => [response.data, ...prev])
        toast.success('Document uploaded successfully!')
      } catch (error: any) {
        toast.error(error.response?.data?.detail || 'Failed to upload document')
      } finally {
        setUploading(false)
      }
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
      'text/markdown': ['.md']
    },
    maxSize: 10 * 1024 * 1024,
  })

  const deleteDocument = async (id: number) => {
    if (!confirm('Are you sure you want to delete this document?')) return
    
    try {
      await documentsAPI.delete(id)
      setDocuments(prev => prev.filter(d => d.id !== id))
      toast.success('Document deleted')
    } catch (error) {
      toast.error('Failed to delete document')
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
  }

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Documents</h1>
        <p className="text-slate-400">Upload and manage your documents for Q&A.</p>
      </div>

      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-all ${
          isDragActive
            ? 'border-cyan-500 bg-cyan-500/10'
            : 'border-slate-600 hover:border-cyan-500/50'
        }`}
      >
        <input {...getInputProps()} />
        <div className="flex flex-col items-center">
          {uploading ? (
            <FiLoader className="text-cyan-400 text-4xl animate-spin mb-4" />
          ) : (
            <FiUpload className="text-slate-400 text-4xl mb-4" />
          )}
          <p className="text-white text-lg mb-2">
            {uploading ? 'Uploading...' : isDragActive ? 'Drop files here' : 'Drag & drop files here'}
          </p>
          <p className="text-slate-500 text-sm">
            or click to select files (PDF, TXT, MD - max 10MB)
          </p>
        </div>
      </div>

      <div className="card p-6">
        <h2 className="text-xl font-semibold text-white mb-6">Your Documents</h2>

        {loading ? (
          <div className="flex justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-cyan-500"></div>
          </div>
        ) : documents.length === 0 ? (
          <div className="text-center py-8">
            <FiFileText className="text-slate-600 text-4xl mx-auto mb-4" />
            <p className="text-slate-400">No documents uploaded yet</p>
          </div>
        ) : (
          <div className="space-y-3">
            <AnimatePresence>
              {documents.map((doc) => (
                <motion.div
                  key={doc.id}
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="flex items-center justify-between p-4 rounded-lg bg-white/5"
                >
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-lg bg-cyan-500/20 flex items-center justify-center">
                      <FiFileText className="text-cyan-400 text-xl" />
                    </div>
                    <div>
                      <p className="text-white font-medium">{doc.title}</p>
                      <p className="text-slate-500 text-sm">
                        {doc.file_name} • {formatFileSize(doc.file_size)} • {formatDate(doc.created_at)}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2">
                      {doc.status === 'completed' ? (
                        <FiCheck className="text-green-400" />
                      ) : (
                        <FiLoader className="text-yellow-400 animate-spin" />
                      )}
                      <span className={`text-sm ${
                        doc.status === 'completed' ? 'text-green-400' : 'text-yellow-400'
                      }`}>
                        {doc.status === 'completed' ? `${doc.chunk_count} chunks` : doc.status}
                      </span>
                    </div>
                    <button
                      onClick={() => deleteDocument(doc.id)}
                      className="p-2 text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
                    >
                      <FiTrash2 />
                    </button>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        )}
      </div>
    </div>
  )
}
