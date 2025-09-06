import { Link } from 'react-router-dom'

export default function Page({children,role,onLogout}:{children:any,role:string,onLogout:()=>void}){
  return (
    <div className="row" style={{height:'100vh'}}>
      <aside className="sidebar">
        <div className="card" style={{fontWeight:700, marginBottom:8}}>AWR</div>
        {role!=="crew" && <Link to="/tasks" className="btn">Задачи</Link>}
        {role==="crew" && <Link to="/my/tasks" className="btn">Мои задачи</Link>}
        <Link to="/access" className="btn">Доступ инфо</Link>
        <Link to="/handover" className="btn">Дома на сдачу</Link>
        {role!=="crew" && <Link to="/inventory" className="btn">Склад</Link>}
        {(role==="admin" || role==="super_admin") && <Link to="/users" className="btn">Пользователи</Link>}
        <button className="btn" onClick={onLogout} style={{marginTop:8}}>Выйти</button>
      </aside>
      <main className="col" style={{flex:1, padding:16, overflow:'auto'}}>
        {children}
      </main>
    </div>
  )
}
