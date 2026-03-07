import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import toast from 'react-hot-toast'
import { FiMail, FiLock, FiUser, FiArrowRight } from 'react-icons/fi'

export default function Register() {
  const [email, setEmail] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [loading, setLoading] = useState(false)
  const { register } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      await register({ email, username, password, full_name: fullName })
      toast.success('Account created! Please login.')
      navigate('/login')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-1/4 left-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl"></div>
      </div>

      <div className="relative w-full max-w-md">
        <div className="card p-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold gradient-text mb-2">Join RAG AI</h1>
            <p className="text-slate-400">Create your account to get started</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm text-slate-400 mb-2">Username</label>
              <div className="relative">
                <FiUser className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" />
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="input-field w-full pl-12 pr-4 py-3 rounded-lg text-white placeholder-slate-500"
                  placeholder="Choose a username"
                  required
                  minLength={3}
                />
              </div>
            </div>

            <div>
              <label className="block text-sm text-slate-400 mb-2">Full Name (optional)</label>
              <div className="relative">
                <FiUser className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" />
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="input-field w-full pl-12 pr-4 py-3 rounded-lg text-white placeholder-slate-500"
                  placeholder="Your name"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm text-slate-400 mb-2">Email</label>
              <div className="relative">
                <FiMail className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="input-field w-full pl-12 pr-4 py-3 rounded-lg text-white placeholder-slate-500"
                  placeholder="Enter your email"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm text-slate-400 mb-2">Password</label>
              <div className="relative">
                <FiLock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="input-field w-full pl-12 pr-4 py-3 rounded-lg text-white placeholder-slate-500"
                  placeholder="Create a password"
                  required
                  minLength={8}
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full py-3 rounded-lg text-white font-semibold flex items-center justify-center gap-2"
            >
              {loading ? (
                <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></div>
              ) : (
                <>
                  Create Account
                  <FiArrowRight />
                </>
              )}
            </button>
          </form>

          <p className="text-center text-slate-400 mt-6">
            Already have an account?{' '}
            <Link to="/login" className="text-cyan-400 hover:underline">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
