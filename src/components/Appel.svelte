<script>
  import { depute } from "./stores";
  import { trackAction } from "./tracking";
  import { isMobile } from "./utils";

  const click = e => {
    if (isMobile()) {
      trackAction("CliquerNumero", `tel:${$depute.telephone_as_e164}`);
    } else {
      e.preventDefault();
    }
  };
</script>

<h4 class="sl">
  j'appelle
  <span class="depute_nom">{$depute.nom}</span>
</h4>
<div class="d-flex mt-3">
  <i class="d-block fa fa-phone mb-2 fa-3x mr-3" />
  <h2 class="depute_numero">
    <a on:click={click} href="tel:{$depute.telephone_as_e164}">
      {$depute.telephone_as_national}
    </a>
  </h2>
</div>
