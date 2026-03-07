import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { documentsAPI, chatAPI } from '../services/api'
import toast from 'react-hot-toast'
import ReactMarkdown from 'react-markdown'
import { FiSend, FiFileText, FiMessageSquare, FiUser, FiBot } from 'react-icons/fi'
import { motion } from 'framer-motion'

interface Document {
  id: number
  title: string
  file_name: string
  status: string
}

interface Message {
  id: number
  role: 'user' | 'assistant'
  content: string
}

interface ChatResponse {
  answer: string
  conversation_id: number
  sources: string[]
  model: string
}

export default function Chat() {
  const { documentId } = useParams<{ documentId?: string }>()
  const navigate = useNavigate()
  const [documents, setDocuments] = useState<Document[]>([])
  const [selectedDoc, setSelectedDoc] = useState<number | null>(null)
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)
  const [answer, setAnswer] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    loadDocuments()
  }, [])

  useEffect(() => {
    if (documentId) {
      setSelectedDoc(parseInt(documentId))
    }
  }, [documentId])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, answer])

  const loadDocuments = async () => {
    try {
      const response = await documentsAPI.list()
      const completed = response.data.filter((d: Document) => d.status === 'completed')
      setDocuments(completed)
      
      if (!selectedDoc && completed.length > 0) {
        setSelectedDoc(completed[0].id)
      }
    } catch (error) {
      console.error('Failed to load documents')
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!selectedDoc) {
      toast.error('Please select a document')
      return
    }
    
    if (!question.trim()) {
      toast.error('Please enter a question')
      return
    }

    const userMessage: Message = {
      id: Date.now(),
      role: 'user',
      content: question
    }
    
    setMessages(prev => [...prev, userMessage])
    setQuestion('')
    setLoading(true)
    setAnswer('')

    try {
      const response = await chatAPI.query(selectedDoc, question)
      const data: ChatResponse = response.data
      
      setAnswer(data.answer)
      
      const assistantMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.answer
      }
      setMessages(prev => [...prev, assistantMessage])
      
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to get answer')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-[calc(100vh-4rem)] flex flex-col">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-white mb-2">Chat with Documents</h1>
        <p className="text-slate-400">Ask questions about your uploaded documents.</p>
      </div>

      <div className="flex gap-6 flex-1 min-h-0">
        <div className="w-72 shrink-0">
          <div className="card p-4 h-full overflow-auto">
            <h3 className="text-white font-semibold mb-4 flex items-center gap-2">
              <FiFileText /> Documents
            </h3>
            
            {documents.length === 0 ? (
              <p className="text-slate-500 text-sm">No documents available</p>
            ) : (
              <div className="space-y-2">
                {documents.map(doc => (
                  <button
                    key={doc.id}
                    onClick={() => {
                      setSelectedDoc(doc.id)
                      navigate(`/chat/${doc.id}`)
                    }}
                    className={`w-full text-left p-3 rounded-lg transition-all ${
                      selectedDoc === doc.id
                        ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30'
                        : 'bg-white/5 text-slate-400 hover:bg-white/10'
                    }`}
                  >
                    <p className="font-medium truncate">{doc.title}</p>
                    <p className="text-xs text-slate-500 truncate">{doc.file_name}</p>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="flex-1 flex flex-col min-h-0">
          <div className="card flex-1 flex flex-col min-h-0 overflow-hidden">
            <div className="flex-1 overflow-auto p-6 space-y-4">
              {messages.length === 0 && !loading && (
                <div className="flex flex-col items-center justify-center h-full text-center">
                  <FiMessageSquare className="text-slate-600 text-5xl mb-4" />
                  <p className="text-slate-400 mb-2">Start a conversation</p>
                  <p className="text-slate-500 text-sm">
                    Select a document and ask questions about its content
                  </p>
                </div>
              )}
              
              {messages.map((msg) => (
                <motion.div
                  key={msg.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
                >
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
                    msg.role === 'user' 
                      ? 'bg-indigo-500/20 text-indigo-400' 
                      : 'bg-cyan-500/20 text-cyan-400'
                  }`}>
                    {msg.role === 'user' ? <FiUser size={14} /> : <FiBot size={14} />}
                  </div>
                  <div className={`max-w-[70%] p-4 rounded-2xl ${
                    msg.role === 'user'
                      ? 'bg-indigo-500/20 text-white'
                      : 'bg-white/5 text-white'
                  }`}>
                    <div className="prose prose-invert prose-sm max-w-none">
                      <ReactMarkdown>{msg.content}</ReactMarkdown>
                    </div>
                  </div>
                </motion.div>
              ))}
              
              {loading && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex gap-3"
                >
                  <div className="w-8 h-8 rounded-full bg-cyan-500/20 flex items-center justify-center">
                    <FiBot size={14} className="text-cyan-400" />
                  </div>
                  <div className="bg-white/5 p-4 rounded-2xl">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                      <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                      <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                    </div>
                  </div>
                </motion.div>
              )}
              
              <div ref={messagesEndRef} />
            </div>

            <form onSubmit={handleSubmit} className="p-4 border-t border-white/10">
              <div className="flex gap-3">
                <input
                  type="text"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="Ask a question about your document..."
                  className="input-field flex-1 px-4 py-3 rounded-xl text-white placeholder-slate-500"
                  disabled={loading || !selectedDoc}
                />
                <button
                  type="submit"
                  disabled={loading || !selectedDoc}
                  className="btn-primary px-6 rounded-xl flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <FiSend />
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}
