import { useEffect, useState } from 'react'
import { api } from '../../lib/api'

export default function MyTasks(){
  const [items,setItems]=useState<any[]>([])
  const [report,setReport]=useState<any>({comment:'',access_info:'',photo_url:'',materials_used:''})
  const [activeId,setActiveId]=useState<number|undefined>()

  async function load(){
    const {data}=await api.get('/tasks/',{params:{status:'in_progress'}})
    setItems(data)
  }
  useEffect(()=>{load()},[])

  async function savePart(task_id:number, part:number){
    await api.post('/reports/upsert', {task_id, crew_id: 3, ...report}, {params:{part}})
    setReport({...report, ...(part===1?{comment:''}:{}) , ...(part===2?{access_info:''}:{}) , ...(part===3?{photo_url:''}:{}) , ...(part===4?{materials_used:''}:{})})
  }

  return (
    <div className="grid" style={{gap:12}}>
      {items.map(t=> (
        <div key={t.id} className="card">
          <div className={`status ${t.status}`}>{t.status}</div>
          <div style={{fontWeight:700}}>{t.address}</div>
          <button className="btn" onClick={()=>setActiveId(activeId===t.id?undefined:t.id)}>{activeId===t.id?'Скрыть отчёт':'Открыть отчёт'}</button>
          {activeId===t.id && (
            <div className="grid" style={{gap:8, marginTop:12}}>
              <textarea className="input" placeholder="Комментарий" value={report.comment} onChange={e=>setReport({...report,comment:e.target.value})}/>
              <button className="btn" onClick={()=>savePart(t.id,1)}>Сохранить часть 1</button>
              <textarea className="input" placeholder="Доступ" value={report.access_info} onChange={e=>setReport({...report,access_info:e.target.value})}/>
              <button className="btn" onClick={()=>savePart(t.id,2)}>Сохранить часть 2</button>
              <input className="input" placeholder="Фото (URL)" value={report.photo_url} onChange={e=>setReport({...report,photo_url:e.target.value})}/>
              <button className="btn" onClick={()=>savePart(t.id,3)}>Сохранить часть 3</button>
              <textarea className="input" placeholder="Списать материалы" value={report.materials_used} onChange={e=>setReport({...report,materials_used:e.target.value})}/>
              <button className="btn" onClick={()=>savePart(t.id,4)}>Сохранить часть 4</button>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
