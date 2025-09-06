export function getTelegram(){
  if(typeof window === 'undefined') return null
  // @ts-ignore
  return window.Telegram?.WebApp ?? null
}

export function getTelegramUserId(): string | null {
  const tg = getTelegram()
  if(tg?.initDataUnsafe?.user?.id){
    return String(tg.initDataUnsafe.user.id)
  }
  return null
}
