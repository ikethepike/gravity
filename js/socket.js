const ws = new WebSocket('ws://localhost:1337')
let interval = null

window.pressed = false

ws.onopen = () => {
  console.log('Connected!')

  interval = setInterval(() => {
    console.log('dispatching request')

    // Dispatch request
    ws.send('poll:request')
  }, 66)
}

ws.onmessage = event => {
  console.log(`Messaged received`)

  const { data } = event

  window.pressed = Boolean(data)
}

ws.onclose = () => {
  window.pressed = false

  clearInterval(interval)
}

ws.onerror = event => {
  console.error('Failed to connected to WS server', event)
}
