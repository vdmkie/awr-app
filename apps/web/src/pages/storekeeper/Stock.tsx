import { useEffect, useState } from 'react'
import { api } from '../../lib/api'

export default function Stock(){
  const [sum,setSum]=useState<any>({materials:[], tools:[]})
  const [move,setMove]=useState<any>({material_id:'',qty:'',from_user_id:'',to_user_id:''})
  const [mat,setMat]=useState<any>({name:'',unit:'m',qty:''})
  const [tool,setTool]=useState<any>({name:'',serial:'',holder_user_id:''})

  async function load(){
    const {data}=await api.get('/inventory/warehouse/summary')
    setSum(data)
  }
  useEffect(()=>{load()},[])

  async function addMaterial(){
    await api.post('/inventory/materials/add',{name:mat.name,unit:mat.unit,qty:Number(mat.qty)})
    setMat({name:'',unit:'m',qty:''}); load()
  }
  async function moveMaterial(){
    await api.post('/inventory/materials/move',{
      material_id:Number(move.material_id), qty:Number(move.qty),
      from_user_id: move.from_user_id? Number(move.from_user_id): null,
      to_user_id: move.to_user_id? Number(move.to_user_id): null,
    })
    setMove({material_id:'',qty:'',from_user_id:'',to_user_id:''}); load()
  }
  async function addTool(){
    await api.post('/inventory/tools/add',{name:tool.name,serial:tool.serial,holder_user_id:tool.holder_user_id?Number(tool.holder_user_id):null})
    setTool({name:'',serial:'',holder_user_id:''}); load()
  }

  return (
    <div className="grid" style={{gap:16}}>
      <div className="row" style={{gap:12, flexWrap:'wrap'}}>
        <a className="btn" href={`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'}/inventory/export.csv`} target="_blank">Экспорт CSV</a>
        <button className="btn" onClick={load}>Обновить</button>
      </div>

      <div className="card grid" style={{gap:8}}>
        <div style={{fontWeight:700}}>Добавить материал</div>
        <div className="row">
          <input className="input" placeholder="Название" value={mat.name} onChange={e=>setMat({...mat,name:e.target.value})}/>
          <select className="input" value={mat.unit} onChange={e=>setMat({...mat,unit:e.target.value})}>
            <option value="m">м</option>
            <option value="pcs">шт</option>
            <option value="kg">кг</option>
          </select>
          <input className="input" placeholder="Кол-во" value={mat.qty} onChange={e=>setMat({...mat,qty:e.target.value})}/>
          <button className="btn" onClick={addMaterial}>Добавить</button>
        </div>
      </div>

      <div className="card grid" style={{gap:8}}>
        <div style={{fontWeight:700}}>Перемещение материалов</div>
        <div className="row">
          <input className="input" placeholder="ID материала" value={move.material_id} onChange={e=>setMove({...move,material_id:e.target.value})}/>
          <input className="input" placeholder="Кол-во" value={move.qty} onChange={e=>setMove({...move,qty:e.target.value})}/>
          <input className="input" placeholder="from_user_id (опц)" value={move.from_user_id} onChange={e=>setMove({...move,from_user_id:e.target.value})}/>
          <input className="input" placeholder="to_user_id (опц)" value={move.to_user_id} onChange={e=>setMove({...move,to_user_id:e.target.value})}/>
          <button className="btn" onClick={moveMaterial}>OK</button>
        </div>
      </div>

      <div className="card grid" style={{gap:8}}>
        <div style={{fontWeight:700}}>Инструменты</div>
        <div className="row">
          <input className="input" placeholder="Название" value={tool.name} onChange={e=>setTool({...tool,name:e.target.value})}/>
          <input className="input" placeholder="Серийный №" value={tool.serial} onChange={e=>setTool({...tool,serial:e.target.value})}/>
          <input className="input" placeholder="holder_user_id (опц)" value={tool.holder_user_id} onChange={e=>setTool({...tool,holder_user_id:e.target.value})}/>
          <button className="btn" onClick={addTool}>Добавить инструмент</button>
        </div>
      </div>

      <div className="grid" style={{gridTemplateColumns:'repeat(auto-fill,minmax(280px,1fr))'}}>
        {sum.materials.map((m:any)=>(
          <div key={m.id} className="card">
            <div style={{fontWeight:700}}>{m.name}</div>
            <div className="badge">{m.qty} {m.unit}</div>
          </div>
        ))}
      </div>

      <div className="grid" style={{gridTemplateColumns:'repeat(auto-fill,minmax(320px,1fr))'}}>
        {sum.tools.map((t:any)=>(
          <div key={t.id} className="card">
            <div style={{fontWeight:700}}>{t.name}</div>
            <div>SN: {t.serial}</div>
            <div className="badge">holder: {t.holder_user_id||'-'}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
