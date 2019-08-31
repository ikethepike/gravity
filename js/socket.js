const ws = new WebSocket('ws://localhost:1337')
let interval = null

window.pressed = false

ws.onopen = () => {
  console.log('Connected!')

  interval = setInterval(() => {
    // Dispatch request
    ws.send('poll:request')
  }, 66)
}

ws.onmessage = event => {
  const { data } = event

  const input = JSON.parse(data).pressed

  window.pressed = Boolean(input)
}

ws.onclose = () => {
  window.pressed = false

  clearInterval(interval)
}

ws.onerror = event => {
  console.error('Failed to connected to WS server', event)
}
