import { FormEvent, useState } from 'react'
import { api, setToken } from '../lib/api'

export default function Login({ onLogin }:{ onLogin:(u:any,t:string)=>void }){
  const [login,setLogin]=useState('')
  const [password,setPassword]=useState('')
  const [loading,setLoading]=useState(false)
  const [error,setError]=useState('')

  async function submit(e:FormEvent){
    e.preventDefault(); setLoading(true); setError('')
    try{
      const form = new FormData(); form.append('username',login); form.append('password',password)
      const {data:tok} = await api.post('/auth/token', form)
      setToken(tok.access_token)
      const {data:me} = await api.get('/auth/me')
      onLogin(me,tok.access_token)
    }catch(err:any){ setError(err?.response?.data?.detail||'Ошибка входа') }
    finally{ setLoading(false) }
  }

  return (
    <div style={{display:'grid', placeItems:'center', height:'100vh'}}>
      <div className="card" style={{width:420}}>
        <div style={{fontWeight:800, fontSize:24, marginBottom:8}}>AWR</div>
        <form onSubmit={submit} className="grid" style={{gap:12}}>
          <input className="input" placeholder="Логин" value={login} onChange={e=>setLogin(e.target.value)} />
          <input className="input" type="password" placeholder="Пароль" value={password} onChange={e=>setPassword(e.target.value)} />
          {error && <div style={{color:'#ef4444'}}>{error}</div>}
          <button className="btn" disabled={loading}>{loading?'Входим...':'Войти'}</button>
        </form>
        <div className="badge" style={{marginTop:8}}>Демо: sa/a1/b1/b2/sk1, пароль 1 (после /auth/seed)</div>
      </div>
    </div>
  )
}
