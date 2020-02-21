<script>
  import { depute } from "./stores";
  import { trackAction } from "./tracking";
</script>

<h4 class="sl">
  j'appelle
  <span class="depute_nom">{$depute.nom}</span>
</h4>
<div class="d-flex mt-3">
  <i class="d-block fa fa-phone mb-2 fa-3x mr-3" />
  <h2 class="depute_numero">
    <a
      on:click={() => trackAction('CliquerNumero', `tel:${$depute.telephone_as_e164}`)}
      href="tel:{$depute.telephone_as_e164}">
      {$depute.telephone_as_national}
    </a>
  </h2>
</div>
