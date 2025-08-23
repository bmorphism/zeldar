(** Model Context Protocol implementation for OCaml *)

(** Protocol version *)
val protocol_version : string

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
val create_message : ?id:message_id -> method_:string -> ?params:Yojson.Safe.t -> unit -> Yojson.Safe.t message

(** Convert message to JSON *)
val message_to_json : Yojson.Safe.t message -> Yojson.Safe.t

(** Parse JSON to message *)
val message_of_json : Yojson.Safe.t -> Yojson.Safe.t message

(** MCP Server interface *)
module Server : sig
  type t

  val create : unit -> t
  val add_resource : t -> resource -> unit
  val add_tool : t -> tool -> unit
  val is_initialized : t -> bool
  val set_initialized : t -> unit
end

