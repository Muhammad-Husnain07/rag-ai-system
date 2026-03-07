import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import toast from 'react-hot-toast'
import { FiMail, FiLock, FiArrowRight } from 'react-icons/fi'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      await login(email, password)
      toast.success('Welcome back!')
      navigate('/')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl"></div>
      </div>

      <div className="relative w-full max-w-md">
        <div className="card p-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold gradient-text mb-2">RAG AI</h1>
            <p className="text-slate-400">Welcome back! Sign in to continue</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
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
                  placeholder="Enter your password"
                  required
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
                  Sign In
                  <FiArrowRight />
                </>
              )}
            </button>
          </form>

          <p className="text-center text-slate-400 mt-6">
            Don't have an account?{' '}
            <Link to="/register" className="text-cyan-400 hover:underline">
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
