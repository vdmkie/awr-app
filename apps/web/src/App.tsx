import { useEffect, useState } from 'react'
import { Route, Routes, useNavigate } from 'react-router-dom'
import Login from './auth/Login'
import Page from './layout/Page'
import Tasks from './pages/superadmin/Tasks'
import MyTasks from './pages/crew/MyTasks'
import Access from './pages/common/Access'
import Handover from './pages/common/Handover'
import Stock from './pages/storekeeper/Stock'
import Users from './pages/admin/Users'
import { api, setToken } from './lib/api'
import { getTelegramUserId } from './lib/telegram'

export default function App(){
  const [user,setUser]=useState<any|null>(null)
  const nav = useNavigate()

  function onLogout(){ setUser(null); localStorage.removeItem('user'); setToken(undefined); nav('/') }

  useEffect(()=>{
    const u = localStorage.getItem('user')
    if(u) setUser(JSON.parse(u))
  },[])

  useEffect(()=>{
    if(user) return
    const tgId = getTelegramUserId()
    if(tgId){
      api.post('/auth/tg_login', null, {params:{tg_id: tgId}})
        .then(async ({data})=>{
          setToken(data.access_token)
          const {data:me} = await api.get('/auth/me')
          setUser(me); localStorage.setItem('user', JSON.stringify(me))
        }).catch(()=>{})
    }
  },[user])

  if(!user){
    return <Login onLogin={(u,t)=>{ setUser(u); localStorage.setItem('user', JSON.stringify(u)) }}/>
  }

  return (
    <Page role={user.role} onLogout={onLogout}>
      <Routes>
        <Route path="/" element={<div className="card">Добро пожаловать, {user.login}</div>} />
        {user.role!=="crew" && <Route path="/tasks" element={<Tasks/>}/>}
        {user.role==="crew" && <Route path="/my/tasks" element={<MyTasks/>}/>}
        <Route path="/access" element={<Access/>} />
        <Route path="/handover" element={<Handover/>} />
        {user.role!=="crew" && <Route path="/inventory" element={<Stock/>} />}
        {(user.role==="admin" || user.role==="super_admin") && <Route path="/users" element={<Users/>} />}
        <Route path="*" element={<div>Страница в разработке</div>} />
      </Routes>
    </Page>
  )
}
