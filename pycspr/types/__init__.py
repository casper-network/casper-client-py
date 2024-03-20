from pycspr.types import cl

from pycspr.types.deploys import Deploy
from pycspr.types.deploys import DeployApproval
from pycspr.types.deploys import DeployArgument
from pycspr.types.deploys import DeployBody
from pycspr.types.deploys import DeployHeader
from pycspr.types.deploys import DeployParameters
from pycspr.types.deploys import DeployTimeToLive
from pycspr.types.deploys import DeployExecutableItem
from pycspr.types.deploys import ModuleBytes
from pycspr.types.deploys import StoredContract
from pycspr.types.deploys import StoredContractByHash
from pycspr.types.deploys import StoredContractByHashVersioned
from pycspr.types.deploys import StoredContractByName
from pycspr.types.deploys import StoredContractByNameVersioned
from pycspr.types.deploys import Transfer

from pycspr.types.identifiers import AccountID
from pycspr.types.identifiers import BlockID
from pycspr.types.identifiers import ContractID
from pycspr.types.identifiers import ContractVersion
from pycspr.types.identifiers import DeployID
from pycspr.types.identifiers import DictionaryID
from pycspr.types.identifiers import DictionaryID_AccountNamedKey
from pycspr.types.identifiers import DictionaryID_ContractNamedKey
from pycspr.types.identifiers import DictionaryID_SeedURef
from pycspr.types.identifiers import DictionaryID_UniqueKey
from pycspr.types.identifiers import Digest
from pycspr.types.identifiers import GlobalStateID
from pycspr.types.identifiers import GlobalStateIDType
from pycspr.types.identifiers import PurseID
from pycspr.types.identifiers import PurseIDType
from pycspr.types.identifiers import StateRootID

from pycspr.types.keys import PrivateKey
from pycspr.types.keys import PublicKey

from pycspr.types.timestamp import Timestamp


DEPLOY_EXECUTABLE_ITEM_VARIANTS = (
    ModuleBytes,
    StoredContractByHash,
    StoredContractByHashVersioned,
    StoredContractByName,
    StoredContractByNameVersioned,
    Transfer,
)

DICTIONARY_ID_VARIANTS = (
    DictionaryID_AccountNamedKey,
    DictionaryID_ContractNamedKey,
    DictionaryID_SeedURef,
    DictionaryID_UniqueKey
)
