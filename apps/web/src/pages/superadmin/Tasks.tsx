import { useEffect, useState } from 'react'
import { api } from '../../lib/api'

export default function Tasks(){
  const [items,setItems]=useState<any[]>([])
  const [qStatus,setQStatus]=useState('')
  const [qCrew,setQCrew]=useState('')
  const [form,setForm]=useState<any>({address:'',floors:'',entrances:'',work_type:'',tz:'',access_info:'',note:''})
  const [assign,setAssign]=useState<{task_id?:number, crew_id?:string}>({})

  async function load(){
    const params:any = {}
    if(qStatus) params.status=qStatus
    if(qCrew) params.assigned_crew_id=qCrew
    const {data}=await api.get('/tasks/',{params})
    setItems(data)
  }
  useEffect(()=>{load()},[qStatus,qCrew])

  async function createTask(){
    const payload = {
      ...form,
      floors: form.floors? Number(form.floors): null,
      entrances: form.entrances? Number(form.entrances): null,
    }
    await api.post('/tasks/', payload)
    setForm({address:'',floors:'',entrances:'',work_type:'',tz:'',access_info:'',note:''})
    await load()
  }

  async function assignCrew(){
    if(!assign.task_id || !assign.crew_id) return
    await api.patch(`/tasks/${assign.task_id}/assign`, null, {params:{crew_id: assign.crew_id}})
    setAssign({})
    await load()
  }

  async function setStatus(id:number, status:string){
    await api.patch(`/tasks/${id}/status`, null, {params:{status}})
    await load()
  }

  return (
    <div className="grid" style={{gap:16}}>
      <div className="card grid" style={{gap:8}}>
        <div style={{fontWeight:700}}>Новая задача</div>
        <div className="row">
          <input className="input" placeholder="Адрес" value={form.address} onChange={e=>setForm({...form,address:e.target.value})}/>
          <input className="input" placeholder="Этажей" value={form.floors} onChange={e=>setForm({...form,floors:e.target.value})}/>
          <input className="input" placeholder="Парадных" value={form.entrances} onChange={e=>setForm({...form,entrances:e.target.value})}/>
          <select className="input" value={form.work_type} onChange={e=>setForm({...form,work_type:e.target.value})}>
            <option value="">Вид работ</option>
            <option>воздушка</option>
            <option>перемычка</option>
            <option>растянуть дом</option>
            <option>дом под ключ</option>
            <option>бурение</option>
            <option>сварки</option>
          </select>
        </div>
        <textarea className="input" placeholder="ТЗ" value={form.tz} onChange={e=>setForm({...form,tz:e.target.value})}/>
        <textarea className="input" placeholder="Доступ" value={form.access_info} onChange={e=>setForm({...form,access_info:e.target.value})}/>
        <input className="input" placeholder="Пометка" value={form.note} onChange={e=>setForm({...form,note:e.target.value})}/>
        <button className="btn" onClick={createTask}>Создать</button>
      </div>

      <div className="row">
        <select className="input" value={qStatus} onChange={e=>setQStatus(e.target.value)}>
          <option value="">Все статусы</option>
          <option value="new">Новая</option>
          <option value="in_progress">В работе</option>
          <option value="done">Выполнено</option>
          <option value="postponed">Отложено</option>
          <option value="problematic">Проблемный дом</option>
        </select>
        <input className="input" placeholder="ID бригады" value={qCrew} onChange={e=>setQCrew(e.target.value)} />
        <button className="btn" onClick={load}>Обновить</button>
      </div>

      <div className="grid" style={{gridTemplateColumns:'repeat(auto-fill,minmax(340px,1fr))'}}>
        {items.map(t=> (
          <div key={t.id} className="card grid" style={{gap:8}}>
            <div className={`status ${t.status}`}>{t.status}</div>
            <div style={{fontWeight:700, fontSize:18}}>{t.address}</div>
            <div className="row"><span className="badge">Бригада: {t.assigned_crew_id??'—'}</span></div>
            <div style={{opacity:.85}}>Тип: {t.work_type}</div>
            <div className="row" style={{gap:8, flexWrap:'wrap'}}>
              <select className="input" value={assign.task_id===t.id? (assign.crew_id||'') : ''} onChange={e=>setAssign({task_id:t.id, crew_id:e.target.value})}>
                <option value="">Назначить бригаду…</option>
                <option value="3">3 (пример)</option>
                <option value="4">4 (пример)</option>
              </select>
              <button className="btn" onClick={assignCrew}>OK</button>
              <button className="btn" onClick={()=>setStatus(t.id,'in_progress')}>В работу</button>
              <button className="btn" onClick={()=>setStatus(t.id,'postponed')}>Отложить</button>
              <button className="btn" onClick={()=>setStatus(t.id,'problematic')}>Проблема</button>
              <button className="btn" onClick={()=>setStatus(t.id,'done')}>Закрыть</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
