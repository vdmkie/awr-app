import { useEffect, useState } from 'react'
import { api } from '../../lib/api'

export default function Users(){
  const [users,setUsers]=useState<any[]>([])
  const [editing,setEditing]=useState<any|null>(null)
  const [creating,setCreating]=useState<any|null>(null)

  async function load(){
    const {data}=await api.get('/users/')
    setUsers(data)
  }
  useEffect(()=>{load()},[])

  async function save(){
    if(editing){
      await api.patch(`/users/${editing.id}`, null, {params:{
        phone: editing.phone,
        role: editing.role,
        crew_topic_id: editing.crew_topic_id,
        password: editing.password||undefined
      }})
      setEditing(null)
      await load()
    }
  }

  async function create(){
    if(creating){
      await api.post('/users/', null, {params:{
        login: creating.login,
        password: creating.password,
        phone: creating.phone,
        role: creating.role,
        crew_topic_id: creating.crew_topic_id
      }})
      setCreating(null)
      await load()
    }
  }

  async function remove(id:number){
    if(window.confirm('Удалить пользователя?')){
      await api.delete(`/users/${id}`)
      await load()
    }
  }

  async function reset(id:number){
    if(window.confirm('Сбросить пароль на "1"?')){
      await api.post(`/users/${id}/reset_password`)
      alert('Пароль сброшен на "1"')
    }
  }

  return (
    <div className="grid" style={{gap:12}}>
      <div className="card grid" style={{gap:6}}>
        <div style={{fontWeight:700}}>Создать пользователя</div>
        <input className="input" placeholder="Логин" value={creating?.login||''} onChange={e=>setCreating({...creating,login:e.target.value})}/>
        <input className="input" type="password" placeholder="Пароль" value={creating?.password||''} onChange={e=>setCreating({...creating,password:e.target.value})}/>
        <input className="input" placeholder="Телефон" value={creating?.phone||''} onChange={e=>setCreating({...creating,phone:e.target.value})}/>
        <select className="input" value={creating?.role||'crew'} onChange={e=>setCreating({...creating,role:e.target.value})}>
          <option value="super_admin">Суперадмин</option>
          <option value="admin">Админ</option>
          <option value="crew">Бригада</option>
          <option value="storekeeper">Кладовщик</option>
        </select>
        <input className="input" placeholder="topic_id" value={creating?.crew_topic_id||''} onChange={e=>setCreating({...creating,crew_topic_id:e.target.value})}/>
        <button className="btn" onClick={create}>Создать</button>
      </div>

      {users.map(u=>(
        <div key={u.id} className="card grid" style={{gap:8}}>
          <div><b>{u.login}</b> (id {u.id})</div>
          {editing?.id===u.id ? (
            <div className="grid" style={{gap:6}}>
              <input className="input" placeholder="Телефон" value={editing.phone||''} onChange={e=>setEditing({...editing,phone:e.target.value})}/>
              <select className="input" value={editing.role} onChange={e=>setEditing({...editing,role:e.target.value})}>
                <option value="super_admin">Суперадмин</option>
                <option value="admin">Админ</option>
                <option value="crew">Бригада</option>
                <option value="storekeeper">Кладовщик</option>
              </select>
              <input className="input" placeholder="topic_id" value={editing.crew_topic_id||''} onChange={e=>setEditing({...editing,crew_topic_id:e.target.value})}/>
              <input className="input" type="password" placeholder="Новый пароль (опционально)" value={editing.password||''} onChange={e=>setEditing({...editing,password:e.target.value})}/>
              <button className="btn" onClick={save}>Сохранить</button>
              <button className="btn" onClick={()=>setEditing(null)}>Отмена</button>
            </div>
          ):(
            <div className="row" style={{gap:8,flexWrap:'wrap'}}>
              <div>📞 {u.phone||'-'}</div>
              <div>🎭 {u.role}</div>
              {u.crew_topic_id && <div className="badge">topic: {u.crew_topic_id}</div>}
              <button className="btn" onClick={()=>setEditing(u)}>Редактировать</button>
              <button className="btn" onClick={()=>remove(u.id)}>Удалить</button>
              <button className="btn" onClick={()=>reset(u.id)}>Сбросить пароль</button>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
