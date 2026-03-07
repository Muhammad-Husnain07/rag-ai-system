import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { FiFileText, FiMessageSquare, FiLogOut, FiHome } from 'react-icons/fi'

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen flex">
      <aside className="w-64 glass border-r border-white/10 flex flex-col">
        <div className="p-6">
          <h1 className="text-2xl font-bold gradient-text">RAG AI</h1>
          <p className="text-slate-400 text-sm mt-1">Smart Document Q&A</p>
        </div>

        <nav className="flex-1 px-4">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg mb-2 transition-all ${
                isActive
                  ? 'bg-cyan-500/20 text-cyan-400'
                  : 'text-slate-400 hover:bg-white/5 hover:text-white'
              }`
            }
          >
            <FiHome size={20} />
            Dashboard
          </NavLink>

          <NavLink
            to="/documents"
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg mb-2 transition-all ${
                isActive
                  ? 'bg-cyan-500/20 text-cyan-400'
                  : 'text-slate-400 hover:bg-white/5 hover:text-white'
              }`
            }
          >
            <FiFileText size={20} />
            Documents
          </NavLink>

          <NavLink
            to="/chat"
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg mb-2 transition-all ${
                isActive
                  ? 'bg-cyan-500/20 text-cyan-400'
                  : 'text-slate-400 hover:bg-white/5 hover:text-white'
              }`
            }
          >
            <FiMessageSquare size={20} />
            Chat
          </NavLink>
        </nav>

        <div className="p-4 border-t border-white/10">
          <div className="flex items-center gap-3 mb-4 px-4">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-cyan-500 to-indigo-500 flex items-center justify-center text-white font-semibold">
              {user?.username?.charAt(0).toUpperCase()}
            </div>
            <div>
              <p className="text-white text-sm font-medium">{user?.username}</p>
              <p className="text-slate-500 text-xs">{user?.email}</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="flex items-center gap-3 px-4 py-3 w-full rounded-lg text-red-400 hover:bg-red-500/10 transition-all"
          >
            <FiLogOut size={20} />
            Logout
          </button>
        </div>
      </aside>

      <main className="flex-1 p-8 overflow-auto">
        <Outlet />
      </main>
    </div>
  )
}
