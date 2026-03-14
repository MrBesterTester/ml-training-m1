// Suggested section for samkirk.com page.tsx
// Add this between the existing project sections (e.g., after Photo Fun or before Explorations)
// This follows the exact pattern used by Dance Menu, Photo Fun, Villa Madu Bali, etc.

<section>
  <h2 className="text-2xl font-semibold text-text-primary">
    Hardware Diagnostics LLM
  </h2>
  <p className="mt-1 text-text-secondary">
    Fine-tuned Llama 3.2 3B with LoRA on Apple MLX to create a hardware test
    &amp; diagnostics advisor — bridging 4 decades of Silicon Valley test
    engineering with modern ML.
  </p>
  <ul className="mt-1 list-disc pl-5 text-sm text-text-muted">
    <li>
      LoRA fine-tuning on M1 iMac (16GB) using physics-first training
      data — the model explains <em>why</em> from first principles, not
      just <em>what</em> to do.
    </li>
    <li>
      Built with Apple MLX + mlx-lm, Claude Code, and the do-work / Dylan
      Davis 3-document methodology.
    </li>
  </ul>
  <Link
    href="/ml-training"
    className="mt-2 inline-block font-medium text-accent hover:text-accent-hover"
  >
    See the results &rarr;
  </Link>
</section>
