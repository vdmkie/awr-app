import { useEffect, useState } from 'react'
import { api } from '../../lib/api'

export default function Access(){
  const [items,setItems]=useState<any[]>([])
  const [q,setQ]=useState('')
  const [newRec,setNewRec]=useState({address:'',info:''})

  async function load(){
    const {data}=await api.get('/access/', {params:{q}})
    setItems(data)
  }
  useEffect(()=>{load()},[q])

  async function create(){
    await api.post('/access/', newRec)
    setNewRec({address:'',info:''}); load()
  }

  return (
    <div className="grid">
      <div className="row">
        <input className="input" placeholder="Фильтр по адресу" value={q} onChange={e=>setQ(e.target.value)}/>
        <button className="btn" onClick={load}>Искать</button>
      </div>
      <div className="card grid" style={{gap:8}}>
        <div style={{fontWeight:700}}>Добавить</div>
        <input className="input" placeholder="Адрес" value={newRec.address} onChange={e=>setNewRec({...newRec,address:e.target.value})}/>
        <textarea className="input" placeholder="Инфо о доступе" value={newRec.info} onChange={e=>setNewRec({...newRec,info:e.target.value})}/>
        <button className="btn" onClick={create}>Сохранить</button>
      </div>
      {items.map((i:any)=>(
        <div key={i.id} className="card">
          <div style={{fontWeight:700}}>{i.address}</div>
          <div style={{opacity:.85, whiteSpace:'pre-wrap'}}>{i.info}</div>
        </div>
      ))}
    </div>
  )}
