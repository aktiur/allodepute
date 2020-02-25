<script>
  import { depute, data } from "./stores";
  import { trackAction } from "./tracking";

  const { mailto_qs } = data;
</script>

<h5 class="sl">Je lui envoie aussi un mail</h5>
<a
  id="email-link"
  on:click={() => trackAction('EnvoyerEmail')}
  class="btn-cust b2 my-2 "
  href="mailto:{$depute.email}{mailto_qs}"
  target="_blank"
  style="width: max-content;">
  Je lui envoie un email
</a>
<p>
  Si ce lien ne marche pas, je peux copier/coller le texte de l'email et
  l'adapter à mes besoins :
</p>
<button
  class="btn-cust b2 my-2"
  data-toggle="modal"
  data-target="#contenu-email">
  J'accède au texte de l'email
</button>
