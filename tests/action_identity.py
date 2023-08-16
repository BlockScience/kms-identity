import api

api.database.drop()

def new_obj_from_rid(rid):
    return api.objects.create_object(obj={"rid": rid})["rid"]

def new_edge_from_rids(name, f, t):
    api.assertions.create_directed_assertion(obj={
        "name": name,
        "from": [f],
        "to": [t]
    })

directed_assertion = new_obj_from_rid("means:dir_asrt")
undirected_assertion = new_obj_from_rid("means:und_asrt")

update_assertion = new_obj_from_rid("func:update_assertion")
fork_assertion = new_obj_from_rid("func:fork_assertion")
create_directed_assertion = new_obj_from_rid("func:create_directed_assertion")
create_undirected_assertion = new_obj_from_rid("func:create_undirected_assertion")
update_directed_assertion_members = new_obj_from_rid("func:update_directed_assertion_members")
update_undirected_assertion_members = new_obj_from_rid("func:update_undirected_assertion_members")
delete_assertion = new_obj_from_rid("func:delete_assertion")

new_edge_from_rids("update", directed_assertion, update_assertion)
new_edge_from_rids("update", undirected_assertion, update_assertion)
new_edge_from_rids("update_members", directed_assertion, update_directed_assertion_members)
new_edge_from_rids("update_members", undirected_assertion, update_undirected_assertion_members)
new_edge_from_rids("fork", directed_assertion, fork_assertion)
new_edge_from_rids("fork", undirected_assertion, fork_assertion)
new_edge_from_rids("create", directed_assertion, create_directed_assertion)
new_edge_from_rids("create", undirected_assertion, create_undirected_assertion)
new_edge_from_rids("delete", directed_assertion, delete_assertion)
new_edge_from_rids("delete", undirected_assertion, delete_assertion)