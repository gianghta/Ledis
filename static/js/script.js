$(document).ready(function(){
	let apiUrl;
	if (window.location.hostname == 'localhost'
		|| window.location.hostname == '127.0.0.1'
		|| window.location.hostname == '0.0.0.0'
	) {
	  apiUrl = `${window.location.protocol}//${window.location.hostname}:8000/command`;
	}
	// Production
	else {
		apiUrl = `${window.location.protocol}//${window.location.hostname}/command`;
	}

	$("#command").keydown(function(e){
		// Enter key
		if(e.keyCode == 13){

			$("#command").prop('disabled', true);
			$.ajax({
				url: apiUrl,
				type: "POST",
				data: ({'command': $("#command").val()}),
				success: function(response){
					$("#log").append(
						`<div class="px-6 py-4 text-grey-darker items-center border-b -mx-4">
							<div class="px-4 flex items-center">
								<span class="text-lg text-grey tracking-wide">` + "$ " + $("#command").val() + `</span>
							</div>
							<div class="px-4">
								<div class="bg-grey h-2 w-2 rounded-full mr-2"></div>
								<pre><code class="rounded whitespace-pre-line">` + response + `</code></pre>
							</div>
						</div>`
					);
					$("#command").val("");
					$("#command").prop('disabled', false);
					$("#command").focus();
				},
				error: function(jqXHR, textStatus, errorMessage) {
					$("#log").append(
						`<div class="px-6 py-4 text-grey-darker items-center border-b -mx-4">
							<div class="px-4 flex items-center">
								<span class="text-lg text-grey tracking-wide">` + "$ " + $("#command").val() + `</span>
							</div>
							<div class="px-4">
								<div class="bg-grey h-2 w-2 rounded-full mr-2"></div>
								<pre><code class="rounded whitespace-pre-line">Server Error</code></pre>
							</div>
						</div>`
					);
					$("#command").val("");
					$("#command").prop('disabled', false);
					$("#command").focus();
				},
				fail: function(xhr, textStatus, errorThrown){
					$("#log").append(
						`<div class="px-6 py-4 text-grey-darker items-center border-b -mx-4">
							<div class="px-4 flex items-center">
								<span class="text-lg text-grey tracking-wide">` + "$ " + $("#command").val() + `</span>
							</div>
							<div class="px-4">
								<div class="bg-grey h-2 w-2 rounded-full mr-2"></div>
								<pre><code class="rounded whitespace-pre-line">Server Error</code></pre>
							</div>
						</div>`
					);
					$("#command").val("");
					$("#command").prop('disabled', false);
					$("#command").focus();
		    }
			});
		}
	});
});
