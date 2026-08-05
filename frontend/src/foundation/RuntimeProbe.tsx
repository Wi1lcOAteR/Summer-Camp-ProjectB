import { useState } from 'react';

export function RuntimeProbe() {
  const [count, setCount] = useState(0);

  return (
    <section aria-labelledby="runtime-probe-title">
      <h1 id="runtime-probe-title">Frontend foundation</h1>
      <p aria-live="polite" role="status">Count: {count}</p>
      <button type="button" aria-label="Increment count" onClick={() => setCount((value) => value + 1)}>
        Increment
      </button>
    </section>
  );
}

export default RuntimeProbe;
