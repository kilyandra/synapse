<script>
  let {
    type = "text",
    placeholder = type,
    value = $bindable(""),
    disabled = false,
    onkeydown = () => {},
    inputRef = $bindable(null),
  } = $props();
</script>

<input
  bind:this={inputRef}
  {type}
  {placeholder}
  bind:value
  {disabled}
  {onkeydown}
  class="bg-white card px-4 py-3 outline-none disabled:opacity-50"
/>
