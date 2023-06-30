def run_components(Map args) {
  assert args.components: "run_components should be passed a list of components to run"

  def components_ = args.components
  if (components_ !instanceof List) {
    components_ = [ components_ ]
  }
  assert components_.size() > 0: "pass at least one component to run_components"

  def from_state_ = args.from_state
  def to_state_ = args.to_state
  def filter_ = args.filter
  def id_ = args.id

  workflow run_components_wf {
    take: input_ch
    main:

    // generate one channel per method
    out_chs = components_.collect{ comp_ ->
      def comp_config = comp_.config

      filter_ch = filter_
        ? input_ch | filter{tup ->
          filter_(tup[0], tup[1], comp_config)
        }
        : input_ch
      id_ch = id_
        ? filter_ch | map{tup ->
          // def new_id = id_(tup[0], tup[1], comp_config)
          def new_id = tup[0]
          if (from_state_ instanceof String) {
            new_id = from_state_
          } else if (from_state_ instanceof Closure) {
            new_id = id_(new_id, tup[1], comp_config)
          }
          [new_id] + tup.drop(1)
        }
        : filter_ch
      data_ch = id_ch | map{tup ->
          def new_data = tup[1]
          if (from_state_ instanceof Map) {
            new_data = from_state_.collectEntries{ key0, key1 ->
              [key0, new_data[key1]]
            }
          } else if (from_state_ instanceof List) {
            new_data = from_state_.collectEntries{ key ->
              [key, new_data[key]]
            }
          } else if (from_state_ instanceof Closure) {
            new_data = from_state_(tup[0], new_data, comp_config)
          }
          tup.take(1) + [new_data] + tup.drop(1)
        }
      out_ch = data_ch
        | comp_.run(
          auto: (args.auto ?: [:]) + [simplifyInput: false, simplifyOutput: false]
        )
      post_ch = to_state_
        ? out_ch | map{tup ->
          def new_outputs = tup[1]
          if (to_state_ instanceof Map) {
            new_outputs = to_state_.collectEntries{ key0, key1 ->
              [key0, new_outputs[key1]]
            }
          } else if (to_state_ instanceof List) {
            new_outputs = to_state_.collectEntries{ key ->
              [key, new_outputs[key]]
            }
          } else if (to_state_ instanceof Closure) {
            new_outputs = to_state_(tup[0], new_outputs, comp_config)
          }
          [tup[0], tup[2] + new_outputs] + tup.drop(3)
        }
        : out_ch
      
      post_ch
    }

    // mix all results
    output_ch =
      (out_chs.size == 1)
        ? out_chs[0]
        : out_chs[0].mix(*out_chs.drop(1))

    emit: output_ch
  }

  return run_components_wf
}

def join_states(Closure apply_) {
  workflow join_states_wf {
    take: input_ch
    main:
    output_ch = input_ch
      | toSortedList
      | filter{ it.size() > 0 }
      | map{ tups ->
        def ids = tups.collect{it[0]}
        def states = tups.collect{it[1]}
        apply_(ids, states)
      }

    emit: output_ch
  }
  return join_states_wf
}


class CustomTraceObserver implements nextflow.trace.TraceObserver {
  List traces

  CustomTraceObserver(List traces) {
    this.traces = traces
  }

  @Override
  void onProcessComplete(nextflow.processor.TaskHandler handler, nextflow.trace.TraceRecord trace) {
    traces.add(trace.store.clone())
  }

  @Override
  void onProcessCached(nextflow.processor.TaskHandler handler, nextflow.trace.TraceRecord trace) {
    traces.add(trace.store.clone())
  }
}

def initialize_tracer() {
  def traces = Collections.synchronizedList([])

  // add custom trace observer which stores traces in the traces object
  session.observers.add(new CustomTraceObserver(traces))

  traces
}

def write_json(data, file) {
  assert data: "write_json: data should not be null"
  assert file: "write_json: file should not be null"
  file.write(groovy.json.JsonOutput.toJson(data))
}

def get_publish_dir() {
  return params.containsKey("publish_dir") ? params.publish_dir : 
    params.containsKey("publishDir") ? params.publishDir : 
    null
}