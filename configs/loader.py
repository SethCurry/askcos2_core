import json
import typing as t

from dataclasses import dataclass

class ValidationError(Exception):
  def __init__(self, field: str, message: str):
    super().__init__(f"Field '{field}' is invalid: {message}")
    self.field = field

class RequiredFieldMissingError(ValidationError):
  def __init__(self, field_name: str):
    super().__init__(field_name, "field is required")
    self.field_name = field_name
  
class Validatable[T]:
  def __init__(self, validator: t.Callable[[T], None], required: bool = False):
    self.validator = validator
    self.required = required

  def __call__(self, field_name: str, value: T) -> T:
    if self.required and value is None:
      raise RequiredFieldMissingError(field_name)

    self.validator(value)

    return value

def __repo_validator(repo: str) -> None:
  if not repo.startswith("https://"):
    raise ValueError(f"Invalid repo, should start with 'https://': {repo}")

RepoField = Validatable[str](__repo_validator)

class ModuleStartConfig:
  def __init__(
      self,
      atom_map_indigo: bool = False,
      atom_map_rxnmapper: bool = False,
      atom_map_wln: bool = False,
      cluster: bool = False,
      context_recommender: bool = False,
      count_analogs: bool = False,
      descriptors: bool = False,
      evaluate_reactions: bool = False,
      fast_filter: bool = False,
      forward_augmented_transformer: bool = False,
      forward_graph2smiles: bool = False,
      forward_wldn5: bool = False,
      general_selectivity: bool = False,
      impurity_predictor: bool = False,
      pathway_ranker: bool = False,
      pmi_calculator: bool = False,
      qm_descriptors: bool = False,
      reaction_classification: bool = False,
      retro_augmented_transformer: bool = False,
      retro_graph2smiles: bool = False,
      retro_retrosim: bool = False,
      retro_template_relevance: bool = False,
      scscore: bool = False,
      site_selectivity: bool = False,
      solubility: bool = False,
      tree_search_expand_one: bool = False,
      tree_search_mcts: bool = False,
      tree_search_retro_star: bool = False
  ):
    self.atom_map_indigo = atom_map_indigo
    self.atom_map_rxnmapper = atom_map_rxnmapper
    self.atom_map_wln = atom_map_wln
    self.cluster = cluster
    self.context_recommender = context_recommender
    self.count_analogs = count_analogs
    self.descriptors = descriptors
    self.evaluate_reactions = evaluate_reactions
    self.fast_filter = fast_filter
    self.forward_augmented_transformer = forward_augmented_transformer
    self.forward_graph2smiles = forward_graph2smiles
    self.forward_wldn5 = forward_wldn5
    self.general_selectivity = general_selectivity
    self.impurity_predictor = impurity_predictor
    self.pathway_ranker = pathway_ranker
    self.pmi_calculator = pmi_calculator
    self.qm_descriptors = qm_descriptors
    self.reaction_classification = reaction_classification
    self.retro_augmented_transformer = retro_augmented_transformer
    self.retro_graph2smiles = retro_graph2smiles
    self.retro_retrosim = retro_retrosim
    self.retro_template_relevance = retro_template_relevance
    self.scscore = scscore
    self.site_selectivity = site_selectivity
    self.solubility = solubility
    self.tree_search_expand_one = tree_search_expand_one
    self.tree_search_mcts = tree_search_mcts
    self.tree_search_retro_star = tree_search_retro_star
  
  @staticmethod
  def from_dict(data: t.Dict[str, t.Any]) -> "ModuleStartConfig":
    return ModuleStartConfig(**data)

class GlobalConfig:
  def __init__(
      self,
      require_frontend: bool = False,
      container_runtime: str = "",
      image_policy: str = "",
      enable_gpu: bool = False
  ):
    self.require_frontend = require_frontend
    self.container_runtime = container_runtime
    self.image_policy = image_policy
    self.enable_gpu = enable_gpu
  
  @staticmethod
  def from_dict(data: t.Dict[str, t.Any]) -> "GlobalConfig":
    return GlobalConfig(**data)

class DeploymentConfig:
  def __init__(
      self,
      deployment_config: str = "",
      use_gpu: bool = False,
      ports_to_expose: t.List[int] = list(),
      default_prediction_url: str = "",
      custom_prediction_url: str = "",
      timeout: int = 0,
      available_model_names: t.List[str] = list()
  ):
    self.deployment_config = deployment_config
    self.use_gpu = use_gpu
    self.ports_to_expose = ports_to_expose
    self.default_prediction_url = default_prediction_url
    self.custom_prediction_url = custom_prediction_url
    self.timeout = timeout
    self.available_model_names = available_model_names
  
  @staticmethod
  def from_dict(data: t.Dict[str, t.Any]) -> "DeploymentConfig":
    return DeploymentConfig(**data)

class ModuleConfig:
  def __init__(
      self,
      repo: str = "",
      description: str = "",
      deployment: DeploymentConfig = DeploymentConfig()
  ):
    # Ensure repo URL is valid
    __repo_validator(repo)
    self.repo = repo

    self.description = description
    self.deployment = deployment
  
  @staticmethod
  def from_dict(data: t.Dict[str, t.Any]) -> "ModuleConfig":
    return ModuleConfig(**data)

class UtilConfig:
  def __init__(
      self,
      engine: str = "",
      database: str = "",
      collection: str = ""
  ):
    self.engine = engine
    self.database = database
    self.collection = collection
  
  @staticmethod
  def from_dict(data: t.Dict[str, t.Any]) -> "UtilConfig":
    return UtilConfig(**data)

class HistorianConfig:
  def __init__(
      self,
      engine: str = "",
      database: str = "",
      collection: str = "",
      files: t.List[str] = list()
  ):
    self.engine = engine
    self.database = database
    self.collection = collection
    self.files = files
  
  @staticmethod
  def from_dict(data: t.Dict[str, t.Any]) -> "HistorianConfig":
    return HistorianConfig(**data)

class PricerConfig(UtilConfig):
  def __init__(
      self,
      engine: str = "",
      database: str = "",
      collection: str = "",
      file: str = "",
      precompute_mols: bool = False
  ):
    self.engine = engine
    self.database = database
    self.collection = collection
    self.file = file
    self.precompute_mols = precompute_mols
  
  @staticmethod
  def from_dict(data: t.Dict[str, t.Any]) -> "PricerConfig":
    return PricerConfig(**data)

class ReactionsConfig:
  def __init__(
      self,
      force_recompute_mols: bool = False
  ):
    self.force_recompute_mols = force_recompute_mols
  
  @staticmethod
  def from_dict(data: t.Dict[str, t.Any]) -> "ReactionsConfig":
    return ReactionsConfig(**data)

class SelectivityRefsConfig:
  def __init__(
      self,
      file: str = ""
  ):
    self.file = file
  
  @staticmethod
  def from_dict(data: t.Dict[str, t.Any]) -> "SelectivityRefsConfig":
    return SelectivityRefsConfig(**data)

@dataclass
class Config:
  def __init__(
      self,
      modules_to_start: ModuleStartConfig = ModuleStartConfig(),
      global_config: GlobalConfig = GlobalConfig(),
      atom_map_indigo: ModuleConfig = ModuleConfig(),
      atom_map_rxnmapper: ModuleConfig = ModuleConfig(),
      atom_map_wln: ModuleConfig = ModuleConfig(),
      cluster: ModuleConfig = ModuleConfig(),
      context_recommender: ModuleConfig = ModuleConfig(),
      count_analogs: ModuleConfig = ModuleConfig(),
      descriptors: ModuleConfig = ModuleConfig(),
      evaluate_reactions: ModuleConfig = ModuleConfig(),
      fast_filter: ModuleConfig = ModuleConfig(),
      forward_augmented_transformer: ModuleConfig = ModuleConfig(),
      forward_graph2smiles: ModuleConfig = ModuleConfig(),
      forward_wldn5: ModuleConfig = ModuleConfig(),
      general_selectivity: ModuleConfig = ModuleConfig(),
      impurity_predictor: ModuleConfig = ModuleConfig(),
      pathway_ranker: ModuleConfig = ModuleConfig(),
      pmi_calculator: ModuleConfig = ModuleConfig(),
      qm_descriptors: ModuleConfig = ModuleConfig(),
      reaction_classification: ModuleConfig = ModuleConfig(),
      retro_augmented_transformer: ModuleConfig = ModuleConfig(),
      retro_graph2smiles: ModuleConfig = ModuleConfig(),
      retro_retrosim: ModuleConfig = ModuleConfig(),
      retro_template_relevance: ModuleConfig = ModuleConfig(),
      scscore: ModuleConfig = ModuleConfig(),
      site_selectivity: ModuleConfig = ModuleConfig(),
      solubility: ModuleConfig = ModuleConfig(),
      tree_search_expand_one: ModuleConfig = ModuleConfig(),
      tree_search_mcts: ModuleConfig = ModuleConfig(),
      tree_search_retro_star: ModuleConfig = ModuleConfig(),
      banned_chemicals: UtilConfig = UtilConfig(),
      banned_reactions: UtilConfig = UtilConfig(),
      historian: HistorianConfig = HistorianConfig(),
      pricer: PricerConfig = PricerConfig(),
      reactions: ReactionsConfig = ReactionsConfig(),
      selectivity_refs: SelectivityRefsConfig = SelectivityRefsConfig(),
      tree_search_results_controller: UtilConfig = UtilConfig(),
      user_controller: UtilConfig = UtilConfig(),
      frontend_config_controller: UtilConfig = UtilConfig()
  ):
    self.modules_to_start = modules_to_start
    self.global_config = global_config
    self.atom_map_indigo = atom_map_indigo
    self.atom_map_rxnmapper = atom_map_rxnmapper
    self.atom_map_wln = atom_map_wln
    self.cluster = cluster
    self.context_recommender = context_recommender
    self.count_analogs = count_analogs
    self.descriptors = descriptors
    self.evaluate_reactions = evaluate_reactions
    self.fast_filter = fast_filter
    self.forward_augmented_transformer = forward_augmented_transformer
    self.forward_graph2smiles = forward_graph2smiles
    self.forward_wldn5 = forward_wldn5
    self.general_selectivity = general_selectivity
    self.impurity_predictor = impurity_predictor
    self.pathway_ranker = pathway_ranker
    self.pmi_calculator = pmi_calculator
    self.qm_descriptors = qm_descriptors
    self.reaction_classification = reaction_classification
    self.retro_augmented_transformer = retro_augmented_transformer
    self.retro_graph2smiles = retro_graph2smiles
    self.retro_retrosim = retro_retrosim
    self.retro_template_relevance = retro_template_relevance
    self.scscore = scscore
    self.site_selectivity = site_selectivity
    self.solubility = solubility
    self.tree_search_expand_one = tree_search_expand_one
    self.tree_search_mcts = tree_search_mcts
    self.tree_search_retro_star = tree_search_retro_star
    self.banned_chemicals = banned_chemicals
    self.banned_reactions = banned_reactions
    self.historian = historian
    self.pricer = pricer
    self.reactions = reactions
    self.selectivity_refs = selectivity_refs
    self.tree_search_results_controller = tree_search_results_controller
    self.user_controller = user_controller
    self.frontend_config_controller = frontend_config_controller
  
  @staticmethod
  def from_dict(data: t.Dict[str, t.Any]) -> "Config":
    return Config(
      modules_to_start=ModuleStartConfig.from_dict(data["modules_to_start"]),
      global_config=GlobalConfig.from_dict(data["global_config"]),
      atom_map_indigo=ModuleConfig.from_dict(data["atom_map_indigo"]),
      atom_map_rxnmapper=ModuleConfig.from_dict(data["atom_map_rxnmapper"]),
      atom_map_wln=ModuleConfig.from_dict(data["atom_map_wln"]),
      cluster=ModuleConfig.from_dict(data["cluster"]),
      context_recommender=ModuleConfig.from_dict(data["context_recommender"]),
      count_analogs=ModuleConfig.from_dict(data["count_analogs"]),
      descriptors=ModuleConfig.from_dict(data["descriptors"]),
      evaluate_reactions=ModuleConfig.from_dict(data["evaluate_reactions"]),
      fast_filter=ModuleConfig.from_dict(data["fast_filter"]),
      forward_augmented_transformer=ModuleConfig.from_dict(data["forward_augmented_transformer"]),
      forward_graph2smiles=ModuleConfig.from_dict(data["forward_graph2smiles"]),
      forward_wldn5=ModuleConfig.from_dict(data["forward_wldn5"]),
      general_selectivity=ModuleConfig.from_dict(data["general_selectivity"]),
      impurity_predictor=ModuleConfig.from_dict(data["impurity_predictor"]),
      pathway_ranker=ModuleConfig.from_dict(data["pathway_ranker"]),
      pmi_calculator=ModuleConfig.from_dict(data["pmi_calculator"]),
      qm_descriptors=ModuleConfig.from_dict(data["qm_descriptors"]),
      reaction_classification=ModuleConfig.from_dict(data["reaction_classification"]),
      retro_augmented_transformer=ModuleConfig.from_dict(data["retro_augmented_transformer"]),
      retro_graph2smiles=ModuleConfig.from_dict(data["retro_graph2smiles"]),
      retro_retrosim=ModuleConfig.from_dict(data["retro_retrosim"]),
      retro_template_relevance=ModuleConfig.from_dict(data["retro_template_relevance"]),
      scscore=ModuleConfig.from_dict(data["scscore"]),
      site_selectivity=ModuleConfig.from_dict(data["site_selectivity"]),
      solubility=ModuleConfig.from_dict(data["solubility"]),
      tree_search_expand_one=ModuleConfig.from_dict(data["tree_search_expand_one"]),
      tree_search_mcts=ModuleConfig.from_dict(data["tree_search_mcts"]),
      tree_search_retro_star=ModuleConfig.from_dict(data["tree_search_retro_star"]),
      banned_chemicals=UtilConfig.from_dict(data["banned_chemicals"]),
      banned_reactions=UtilConfig.from_dict(data["banned_reactions"]),
      historian=HistorianConfig.from_dict(data["historian"]),
      pricer=PricerConfig.from_dict(data["pricer"]),
      reactions=ReactionsConfig.from_dict(data["reactions"]),
      selectivity_refs=SelectivityRefsConfig.from_dict(data["selectivity_refs"]),
      tree_search_results_controller=UtilConfig.from_dict(data["tree_search_results_controller"]),
      user_controller=UtilConfig.from_dict(data["user_controller"]),
      frontend_config_controller=UtilConfig.from_dict(data["frontend_config_controller"]),
    )

def load_config(contents: str) -> Config:
  loaded = json.loads(contents)

  return Config.from_dict(loaded)
