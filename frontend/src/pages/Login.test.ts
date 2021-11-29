// NOTE: jest-dom adds handy assertions to Jest and it is recommended, but not required.
import '@testing-library/jest-dom'
import {render, fireEvent} from '@testing-library/svelte'
import Login from './Login.svelte'
import { Button } from "carbon-components-svelte"

// Note: This is as an async test as we are using `fireEvent`
test('button on screen', () => {
    const screen = render(Login)
    console.log("test start 2")
    const btn = screen.getByText('Button')


    // Using await when firing events is unique to the svelte testing library because
    // we have to wait for the next `tick` so that Svelte flushes all pending state changes.
    // await fireEvent.click(button)

    expect(btn).toHaveTextContent('Button')
})