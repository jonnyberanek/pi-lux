import axios from 'axios'
import { RgbColor } from './RgbSlider'

const piDev = true

const URL =
  process.env.NODE_ENV === 'development' && !piDev
    ? 'http://localhost:4061'
    : 'http://192.168.0.175:4061'

    // Mocked currently
export async function getScriptsInDir() {
  return axios.get(URL + '/scripts').then(({ data }) => data)
}

export async function runScript(name: string) {
  return axios.post(`${URL}/scripts/${name.slice(0, name.length-3)}/run`, {})
}

export async function setColor(c: RgbColor) {
  try {
    await axios.post('http://192.168.0.175:4061/testnet', {
      color: [c[0], c[2], c[1]],
    })
  } catch (e) {
    console.log(e.request, e.response)
  }
}