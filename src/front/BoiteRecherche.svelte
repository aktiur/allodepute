<script>
  import { createEventDispatcher } from "svelte";

  let input;
  const dispatch = createEventDispatcher();

  const onSubmit = e => {
    if (!input.value.match(/^[0-9]{5}$/)) {
      input.setCustomValidity(
        "Indiquez un code postal français valide (5 chiffres)"
      );
    } else {
      dispatch("recherche", { codePostal: input.value });
    }
  };
</script>

<div class="form-row">
  <div class="col-auto">
    <form on:submit|preventDefault={onSubmit}>
      <label for="inputcp" class="sr-only">Mon code postal</label>
      <div class="input-group">
        <input
          bind:this={input}
          on:input={() => input.setCustomValidity('')}
          type="search"
          class="form-control"
          id="inputcp"
          placeholder="Mon code postal" />
        <div class="input-group-append">
          <button class="btn btn-primary" type="submit">
            <i class="fa fa-search" />
          </button>
        </div>
      </div>
    </form>
  </div>
</div>
