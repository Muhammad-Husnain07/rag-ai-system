import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { documentsAPI } from '../services/api'
import { FiFileText, FiMessageSquare, FiUpload, FiArrowRight } from 'react-icons/fi'
import { motion } from 'framer-motion'

interface Document {
  id: number
  title: string
  file_name: string
  file_type: string
  status: string
  chunk_count: number
  created_at: string
}

export default function Dashboard() {
  const [documents, setDocuments] = useState<Document[]>([])
  const [loading, setLoading] = useState(true)

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

  const completedDocs = documents.filter(d => d.status === 'completed').length
  const totalChunks = documents.reduce((acc, d) => acc + d.chunk_count, 0)

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Dashboard</h1>
        <p className="text-slate-400">Welcome back! Here's an overview of your documents.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card p-6"
        >
          <div className="flex items-center gap-4">
            <div className="w-14 h-14 rounded-xl bg-cyan-500/20 flex items-center justify-center">
              <FiFileText className="text-cyan-400 text-2xl" />
            </div>
            <div>
              <p className="text-slate-400 text-sm">Total Documents</p>
              <p className="text-3xl font-bold text-white">{documents.length}</p>
            </div>
          </div>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card p-6"
        >
          <div className="flex items-center gap-4">
            <div className="w-14 h-14 rounded-xl bg-green-500/20 flex items-center justify-center">
              <FiUpload className="text-green-400 text-2xl" />
            </div>
            <div>
              <p className="text-slate-400 text-sm">Processed</p>
              <p className="text-3xl font-bold text-white">{completedDocs}</p>
            </div>
          </div>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card p-6"
        >
          <div className="flex items-center gap-4">
            <div className="w-14 h-14 rounded-xl bg-indigo-500/20 flex items-center justify-center">
              <FiMessageSquare className="text-indigo-400 text-2xl" />
            </div>
            <div>
              <p className="text-slate-400 text-sm">Total Chunks</p>
              <p className="text-3xl font-bold text-white">{totalChunks}</p>
            </div>
          </div>
        </motion.div>
      </div>

      <div className="card p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-white">Recent Documents</h2>
          <Link
            to="/documents"
            className="text-cyan-400 hover:text-cyan-300 flex items-center gap-2"
          >
            View all <FiArrowRight />
          </Link>
        </div>

        {loading ? (
          <div className="flex justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-cyan-500"></div>
          </div>
        ) : documents.length === 0 ? (
          <div className="text-center py-8">
            <FiFileText className="text-slate-600 text-4xl mx-auto mb-4" />
            <p className="text-slate-400 mb-4">No documents yet</p>
            <Link
              to="/documents"
              className="btn-primary inline-flex items-center gap-2 px-4 py-2 rounded-lg text-white"
            >
              <FiUpload /> Upload Document
            </Link>
          </div>
        ) : (
          <div className="space-y-3">
            {documents.slice(0, 5).map((doc) => (
              <Link
                key={doc.id}
                to={`/chat/${doc.id}`}
                className="flex items-center justify-between p-4 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
              >
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-lg bg-cyan-500/20 flex items-center justify-center">
                    <FiFileText className="text-cyan-400" />
                  </div>
                  <div>
                    <p className="text-white font-medium">{doc.title}</p>
                    <p className="text-slate-500 text-sm">{doc.file_name}</p>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <span className={`px-3 py-1 rounded-full text-xs ${
                    doc.status === 'completed' 
                      ? 'bg-green-500/20 text-green-400'
                      : 'bg-yellow-500/20 text-yellow-400'
                  }`}>
                    {doc.status}
                  </span>
                  <FiArrowRight className="text-slate-500" />
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
