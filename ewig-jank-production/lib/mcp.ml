(** Model Context Protocol implementation for OCaml *)

(** Protocol version *)
let protocol_version = "2024-11-05"

(** Message types for MCP *)
type message_id = string

type request_method = 
  | Initialize
  | Resources_list
  | Resources_read
  | Tools_list
  | Tools_call
  | Prompts_list
  | Prompts_get
  | Completion_complete
  | Custom of string

type notification_method =
  | Initialized
  | Progress
  | Resource_updated
  | Tool_call_result
  | Custom_notification of string

(** Basic message structure *)
type 'a message = {
  jsonrpc: string;
  id: message_id option;
  method_: string;
  params: 'a option;
}

(** Initialize request parameters *)
type initialize_params = {
  protocol_version: string;
  capabilities: Yojson.Safe.t;
  client_info: Yojson.Safe.t;
}

(** Resource definition *)
type resource = {
  uri: string;
  name: string;
  description: string option;
  mime_type: string option;
}

(** Tool definition *)
type tool = {
  name: string;
  description: string;
  input_schema: Yojson.Safe.t;
}

(** Create a new message *)
let create_message ?id ~method_ ?params () =
  { jsonrpc = "2.0"; id; method_; params }

(** Convert message to JSON *)
let message_to_json msg =
  let base = [
    ("jsonrpc", `String msg.jsonrpc);
    ("method", `String msg.method_);
  ] in
  let with_id = match msg.id with
    | Some id -> ("id", `String id) :: base
    | None -> base
  in
  let with_params = match msg.params with
    | Some params -> ("params", params) :: with_id
    | None -> with_id
  in
  `Assoc with_params

(** Parse JSON to message *)
let message_of_json json =
  let open Yojson.Safe.Util in
  let jsonrpc = json |> member "jsonrpc" |> to_string in
  let id = json |> member "id" |> to_string_option in
  let method_ = json |> member "method" |> to_string in
  let params = json |> member "params" |> function
    | `Null -> None
    | p -> Some p
  in
  { jsonrpc; id; method_; params }

(** MCP Server interface *)
module Server = struct
  type t = {
    resources: resource list ref;
    tools: tool list ref;
    initialized: bool ref;
  }

  let create () = {
    resources = ref [];
    tools = ref [];
    initialized = ref false;
  }

  let add_resource server resource =
    server.resources := resource :: !(server.resources)

  let add_tool server tool =
    server.tools := tool :: !(server.tools)

  let is_initialized server = !(server.initialized)

  let set_initialized server = 
    server.initialized := true
end

