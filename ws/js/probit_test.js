import { WebSocket } from 'ws';

const ws = new WebSocket('wss://api.probit.com/api/exchange/v1/ws');

ws.onopen = () => {
  const msg = {
    type: 'subscribe',
    channel: 'marketdata',
    interval: 500,
    market_id: 'FBX-USDT',
    filter: ['ticker', 'order_books']
  };
  ws.send(JSON.stringify(msg,null,'\t'));
};

ws.onmessage = (event) => {
  console.log(event.data);

  console.log(typeof(event.data))

};