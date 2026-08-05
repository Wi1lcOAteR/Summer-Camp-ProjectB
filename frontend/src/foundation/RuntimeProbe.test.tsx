import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import { RuntimeProbe } from './RuntimeProbe';

describe('RuntimeProbe', () => {
  it('exposes an accessible counter that responds to a real click', async () => {
    const user = userEvent.setup();
    render(<RuntimeProbe />);

    const button = screen.getByRole('button', { name: 'Increment count' });
    expect(button).toBeTruthy();
    expect(screen.getByRole('status').textContent).toBe('Count: 0');

    await user.click(button);

    expect(screen.getByRole('status').textContent).toBe('Count: 1');
  });
});
