<script>
  import { createEventDispatcher } from "svelte";

  export let depute;
  export let i;
  export let extraClasses = "";

  const dispatch = createEventDispatcher();
</script>

<style>
  div.cadre {
    cursor: pointer;
  }
</style>

<div
  class="cadre cadre{i}
  {extraClasses}"
  on:click={() => dispatch('choix', { depute })}>
  <div class="img" style="background-image: var(--cadre), url({depute.image});">
    <div />
  </div>
</div>
