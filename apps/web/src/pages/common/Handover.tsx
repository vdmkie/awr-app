import { useEffect, useState } from 'react'
import { api } from '../../lib/api'

export default function Handover(){
  const [items,setItems]=useState<any[]>([])
  const [form,setForm]=useState({address:'',note:''})

  async function load(){
    const {data}=await api.get('/handover/')
    setItems(data)
  }
  useEffect(()=>{load()},[])

  async function create(){
    await api.post('/handover/', form)
    setForm({address:'',note:''}); load()
  }

  return (
    <div className="grid">
      <div className="card grid" style={{gap:8}}>
        <div style={{fontWeight:700}}>Добавить дом</div>
        <input className="input" placeholder="Адрес" value={form.address} onChange={e=>setForm({...form,address:e.target.value})}/>
        <textarea className="input" placeholder="Примечание" value={form.note} onChange={e=>setForm({...form,note:e.target.value})}/>
        <button className="btn" onClick={create}>Сохранить</button>
      </div>

      {items.map((h:any)=>(
        <div key={h.id} className="card">
          <div style={{fontWeight:700}}>{h.address}</div>
          <div style={{opacity:.85}}>{h.note}</div>
        </div>
      ))}
    </div>
  )
}
